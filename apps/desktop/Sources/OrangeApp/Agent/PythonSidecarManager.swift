import Foundation

final class PythonSidecarManager {
    private var process: Process?
    private var startupTask: Task<Void, Never>?
    private let maxRestartAttempts = 3
    private var restartAttempts = 0
    private var isStopping = false
    private var isStarting = false

    func startIfNeeded() {
        if process?.isRunning == true || isStarting { return }
        restartAttempts = 0
        startProcess()
    }

    private func startProcess() {
        isStarting = true
        isStopping = false

        let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
            .deletingLastPathComponent()
            .deletingLastPathComponent()

        let agentDirectory = repoRoot.appendingPathComponent("agent")
        guard FileManager.default.fileExists(atPath: agentDirectory.path) else {
            Logger.error("agent directory not found at \(agentDirectory.path)")
            return
        }

        let p = Process()
        p.currentDirectoryURL = agentDirectory
        p.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        p.arguments = ["python3", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "7789"]

        let stdout = Pipe()
        let stderr = Pipe()
        p.standardOutput = stdout
        p.standardError = stderr
        attachLogReader(pipe: stdout, stream: "stdout")
        attachLogReader(pipe: stderr, stream: "stderr")
        p.terminationHandler = { [weak self] terminated in
            guard let self else { return }
            Task { @MainActor in
                self.handleTermination(terminated)
            }
        }

        do {
            try p.run()
            process = p
            Logger.info("Sidecar started")
            startupTask?.cancel()
            startupTask = Task { [weak self] in
                guard let self else { return }
                let healthy = await self.waitForHealth(timeoutSeconds: 8)
                await MainActor.run {
                    self.isStarting = false
                    if healthy {
                        self.restartAttempts = 0
                        Logger.info("Sidecar health check passed")
                    } else {
                        Logger.error("Sidecar health check failed")
                        self.restartIfNeeded(reason: "health_check_failed")
                    }
                }
            }
        } catch {
            isStarting = false
            Logger.error("Failed to start sidecar: \(error.localizedDescription)")
            restartIfNeeded(reason: "launch_failed")
        }
    }

    func stop() {
        isStopping = true
        startupTask?.cancel()
        startupTask = nil
        process?.terminate()
        process = nil
        Logger.info("Sidecar stopped")
    }

    private func restartIfNeeded(reason: String) {
        guard !isStopping else { return }
        guard restartAttempts < maxRestartAttempts else {
            Logger.error("Sidecar restart limit reached after reason=\(reason)")
            return
        }
        restartAttempts += 1
        Logger.error("Restarting sidecar (\(restartAttempts)/\(maxRestartAttempts)) reason=\(reason)")
        process?.terminate()
        process = nil
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) { [weak self] in
            self?.startProcess()
        }
    }

    private func handleTermination(_ terminated: Process) {
        guard !isStopping else { return }
        let status = terminated.terminationStatus
        let reason = terminated.terminationReason == .exit ? "exit" : "uncaught_signal"
        Logger.error("Sidecar terminated reason=\(reason) status=\(status)")
        process = nil
        restartIfNeeded(reason: "terminated")
    }

    private func attachLogReader(pipe: Pipe, stream: String) {
        pipe.fileHandleForReading.readabilityHandler = { handle in
            let data = handle.availableData
            guard !data.isEmpty else { return }
            guard let text = String(data: data, encoding: .utf8) else { return }
            let lines = text.split(whereSeparator: \.isNewline)
            for line in lines where !line.isEmpty {
                Logger.info("[sidecar][\(stream)] \(line)")
            }
        }
    }

    private func waitForHealth(timeoutSeconds: Int) async -> Bool {
        let deadline = Date().addingTimeInterval(TimeInterval(timeoutSeconds))
        while Date() < deadline {
            if await isHealthy() {
                return true
            }
            try? await Task.sleep(nanoseconds: 200_000_000)
        }
        return false
    }

    private func isHealthy() async -> Bool {
        guard let url = URL(string: "http://127.0.0.1:7789/health") else {
            return false
        }
        var request = URLRequest(url: url)
        request.timeoutInterval = 0.7
        do {
            let (_, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse else {
                return false
            }
            return http.statusCode == 200
        } catch {
            return false
        }
    }

    deinit {
        stop()
    }
}
