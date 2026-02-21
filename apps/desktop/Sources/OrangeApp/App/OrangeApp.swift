import SwiftUI

@main
struct OrangeApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    @StateObject private var appState = AppState()
    @State private var showOnboarding = false
    @State private var permissionStatus = PermissionsManager.Status(
        accessibility: false,
        microphone: false,
        screenRecording: false
    )

    private let sessionManager: SessionManager
    private let sidecarManager = PythonSidecarManager()
    private let hotkeyManager = HotkeyManager()
    private let permissionsManager = PermissionsManager()

    init() {
        let stt = AppleSpeechRecognizer()
        let context = LocalContextProvider()
        let planner = HTTPPlannerClient()
        let executor = ActionExecutor()
        let safety = DefaultSafetyPolicy()

        self.sessionManager = SessionManager(
            sttService: stt,
            contextProvider: context,
            plannerClient: planner,
            executionEngine: executor,
            safetyPolicy: safety
        )
    }

    var body: some Scene {
        WindowGroup("Orange") {
            OverlayView(
                appState: appState,
                onStart: {
                    sessionManager.beginRecording(state: appState)
                },
                onStop: {
                    Task { await sessionManager.stopRecordingAndPlan(state: appState) }
                },
                onConfirm: {
                    Task { await sessionManager.confirmAndExecute(state: appState) }
                },
                onCancel: {
                    sessionManager.cancel(state: appState)
                }
            )
            .onAppear {
                refreshPermissionStatus()
                sidecarManager.startIfNeeded()
                hotkeyManager.register(
                    onPress: { sessionManager.beginRecording(state: appState) },
                    onRelease: { Task { await sessionManager.stopRecordingAndPlan(state: appState) } }
                )
            }
            .onDisappear {
                sidecarManager.stop()
            }
            .sheet(isPresented: $showOnboarding) {
                OnboardingView(
                    status: permissionStatus,
                    onRequestAccessibility: {
                        _ = permissionsManager.promptAccessibilityPermission()
                        permissionsManager.openSettingsAccessibility()
                    },
                    onRequestMicrophone: {
                        Task {
                            _ = await permissionsManager.requestMicrophonePermission()
                            permissionsManager.openSettingsMicrophone()
                            await MainActor.run {
                                refreshPermissionStatus()
                            }
                        }
                    },
                    onRequestScreenRecording: {
                        _ = permissionsManager.requestScreenRecordingPermission()
                        permissionsManager.openSettingsScreenRecording()
                    },
                    onRefresh: {
                        refreshPermissionStatus()
                    }
                )
            }
        }
        .windowResizability(.contentSize)
        .commands {
            CommandMenu("Orange") {
                Button("Permissions Setup") {
                    refreshPermissionStatus()
                    showOnboarding = true
                }
            }
        }
    }

    private func refreshPermissionStatus() {
        permissionStatus = permissionsManager.currentStatus()
        showOnboarding = !permissionStatus.allGranted
    }
}
