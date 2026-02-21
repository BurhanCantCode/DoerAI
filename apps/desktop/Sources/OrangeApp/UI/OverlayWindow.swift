import AppKit
import SwiftUI

@MainActor
final class OverlayWindow {
    static let shared = OverlayWindow()

    private var panel: NSPanel?

    private init() {}

    func attach<Content: View>(rootView: Content) {
        let panel = panel ?? makePanel()
        panel.contentView = NSHostingView(rootView: rootView)
        self.panel = panel
    }

    func show() {
        guard let panel else { return }
        reposition(panel: panel)
        panel.orderFrontRegardless()
    }

    func hide() {
        panel?.orderOut(nil)
    }

    private func makePanel() -> NSPanel {
        let panel = NSPanel(
            contentRect: NSRect(x: 0, y: 0, width: 520, height: 260),
            styleMask: [.nonactivatingPanel, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )
        panel.level = .floating
        panel.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        panel.isFloatingPanel = true
        panel.hidesOnDeactivate = false
        panel.isOpaque = false
        panel.backgroundColor = .clear
        panel.hasShadow = true
        panel.titleVisibility = .hidden
        panel.titlebarAppearsTransparent = true
        reposition(panel: panel)
        return panel
    }

    private func reposition(panel: NSPanel) {
        guard let frame = NSScreen.main?.visibleFrame else { return }
        let x = frame.midX - panel.frame.width / 2
        let y = frame.maxY - panel.frame.height - 32
        panel.setFrameOrigin(NSPoint(x: x, y: y))
    }
}
