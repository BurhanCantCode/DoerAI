import AppKit

extension Notification.Name {
    static let orangeShowOverlay = Notification.Name("orangeShowOverlay")
    static let orangeShowAPIKeySetup = Notification.Name("orangeShowAPIKeySetup")
    static let orangeShowPermissions = Notification.Name("orangeShowPermissions")
    static let orangeShowDiagnostics = Notification.Name("orangeShowDiagnostics")
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem?

    func applicationDidFinishLaunching(_ notification: Notification) {
        Logger.info("Orange app launched")
        // Prevent app from terminating when windows are hidden
        NSApp.setActivationPolicy(.accessory)
        setupStatusItem()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        false
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)

        if let button = statusItem?.button {
            let image = NSImage(systemSymbolName: "circle.fill", accessibilityDescription: "Orange")
            let config = NSImage.SymbolConfiguration(pointSize: 12, weight: .regular)
            button.image = image?.withSymbolConfiguration(config)
            button.contentTintColor = NSColor(red: 1.0, green: 0.42, blue: 0.0, alpha: 1.0)
        }

        let menu = NSMenu()
        menu.addItem(withTitle: "Show Overlay", action: #selector(showOverlay), keyEquivalent: "")
        menu.addItem(.separator())
        menu.addItem(withTitle: "API Key Setup…", action: #selector(showAPIKeySetup), keyEquivalent: "")
        menu.addItem(withTitle: "Permissions…", action: #selector(showPermissions), keyEquivalent: "")
        menu.addItem(withTitle: "Diagnostics", action: #selector(showDiagnostics), keyEquivalent: "")
        menu.addItem(.separator())
        menu.addItem(withTitle: "Quit Orange", action: #selector(quitApp), keyEquivalent: "q")

        for item in menu.items {
            item.target = self
        }

        statusItem?.menu = menu
    }

    @objc private func showOverlay() {
        NotificationCenter.default.post(name: .orangeShowOverlay, object: nil)
    }

    @objc private func showAPIKeySetup() {
        NotificationCenter.default.post(name: .orangeShowAPIKeySetup, object: nil)
    }

    @objc private func showPermissions() {
        NotificationCenter.default.post(name: .orangeShowPermissions, object: nil)
    }

    @objc private func showDiagnostics() {
        NotificationCenter.default.post(name: .orangeShowDiagnostics, object: nil)
    }

    @objc private func quitApp() {
        NSApplication.shared.terminate(nil)
    }
}
