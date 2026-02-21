import SwiftUI

struct OnboardingView: View {
    let status: PermissionsManager.Status
    let onRequestAccessibility: () -> Void
    let onRequestMicrophone: () -> Void
    let onRequestScreenRecording: () -> Void
    let onRefresh: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Permissions Setup")
                .font(.title2.weight(.semibold))
            Text("Orange needs permissions to read context and execute actions across apps.")
                .font(.subheadline)
                .foregroundStyle(.secondary)

            permissionRow(
                title: "Accessibility",
                granted: status.accessibility,
                actionTitle: "Grant",
                action: onRequestAccessibility
            )

            permissionRow(
                title: "Microphone",
                granted: status.microphone,
                actionTitle: "Grant",
                action: onRequestMicrophone
            )

            permissionRow(
                title: "Screen Recording",
                granted: status.screenRecording,
                actionTitle: "Grant",
                action: onRequestScreenRecording
            )

            HStack {
                Button("Refresh") { onRefresh() }
                Spacer()
                Text(status.allGranted ? "All permissions granted" : "Grant all to continue")
                    .font(.caption)
                    .foregroundStyle(status.allGranted ? .green : .orange)
            }
        }
        .padding(20)
        .frame(width: 500)
    }

    @ViewBuilder
    private func permissionRow(
        title: String,
        granted: Bool,
        actionTitle: String,
        action: @escaping () -> Void
    ) -> some View {
        HStack(spacing: 12) {
            Circle()
                .fill(granted ? Color.green : Color.orange)
                .frame(width: 10, height: 10)
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.body.weight(.medium))
                Text(granted ? "Granted" : "Required")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            if !granted {
                Button(actionTitle, action: action)
            }
        }
    }
}
