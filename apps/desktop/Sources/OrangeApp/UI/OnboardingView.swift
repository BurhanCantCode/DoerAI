import SwiftUI

struct OnboardingView: View {
    let status: PermissionsManager.Status
    let onRequestAccessibility: () -> Void
    let onRequestMicrophone: () -> Void
    let onRequestScreenRecording: () -> Void
    let onRefresh: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            // Orange accent line
            Capsule()
                .fill(Color.orange)
                .frame(width: 32, height: 3)

            Text("ORANGE")
                .font(.system(size: 11, weight: .bold, design: .monospaced))
                .foregroundStyle(.orange)
                .tracking(3)

            Text("Permissions Setup")
                .font(.title2.weight(.semibold))
            Text("Orange needs these permissions to read your screen, hear your voice, and execute actions across apps.")
                .font(.subheadline)
                .foregroundStyle(.secondary)

            VStack(spacing: 10) {
                permissionCard(
                    icon: "hand.raised.fill",
                    title: "Accessibility",
                    description: "Control UI elements across apps",
                    granted: status.accessibility,
                    action: onRequestAccessibility
                )

                permissionCard(
                    icon: "mic.fill",
                    title: "Microphone",
                    description: "Capture voice commands",
                    granted: status.microphone,
                    action: onRequestMicrophone
                )

                permissionCard(
                    icon: "rectangle.dashed.badge.record",
                    title: "Screen Recording",
                    description: "Understand what you're looking at",
                    granted: status.screenRecording,
                    action: onRequestScreenRecording
                )
            }

            HStack {
                Button("Refresh") { onRefresh() }
                    .buttonStyle(.plain)
                    .foregroundStyle(.orange)
                    .font(.subheadline.weight(.medium))
                Spacer()
                HStack(spacing: 4) {
                    Circle()
                        .fill(status.allGranted ? Color.green : Color.orange)
                        .frame(width: 6, height: 6)
                    Text(status.allGranted ? "All permissions granted" : "Grant all to continue")
                        .font(.caption)
                        .foregroundStyle(status.allGranted ? .green : .orange)
                }
            }
        }
        .padding(24)
        .frame(width: 500)
        .preferredColorScheme(.dark)
    }

    @ViewBuilder
    private func permissionCard(
        icon: String,
        title: String,
        description: String,
        granted: Bool,
        action: @escaping () -> Void
    ) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 16))
                .foregroundStyle(granted ? .green : .orange)
                .frame(width: 32, height: 32)
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill((granted ? Color.green : Color.orange).opacity(0.12))
                )
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.body.weight(.medium))
                Text(description)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            if granted {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundStyle(.green)
            } else {
                Button("Grant") { action() }
                    .buttonStyle(.plain)
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 5)
                    .background(Capsule().fill(Color.orange))
            }
        }
        .padding(12)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(white: 0.1))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.white.opacity(0.08), lineWidth: 1)
        )
    }
}
