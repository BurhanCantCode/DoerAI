import SwiftUI

struct NotchShape: Shape {
    var expanded: Bool

    var animatableData: CGFloat {
        get { expanded ? 1 : 0 }
        set { expanded = newValue > 0.5 }
    }

    func path(in rect: CGRect) -> Path {
        if !expanded {
            return Path(roundedRect: rect, cornerRadius: rect.height / 2)
        }

        let topRadius: CGFloat = 10
        let bottomRadius: CGFloat = 22

        var path = Path()
        path.move(to: CGPoint(x: rect.minX + topRadius, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.maxX - topRadius, y: rect.minY))
        path.addArc(tangent1End: CGPoint(x: rect.maxX, y: rect.minY),
                     tangent2End: CGPoint(x: rect.maxX, y: rect.minY + topRadius),
                     radius: topRadius)
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY - bottomRadius))
        path.addArc(tangent1End: CGPoint(x: rect.maxX, y: rect.maxY),
                     tangent2End: CGPoint(x: rect.maxX - bottomRadius, y: rect.maxY),
                     radius: bottomRadius)
        path.addLine(to: CGPoint(x: rect.minX + bottomRadius, y: rect.maxY))
        path.addArc(tangent1End: CGPoint(x: rect.minX, y: rect.maxY),
                     tangent2End: CGPoint(x: rect.minX, y: rect.maxY - bottomRadius),
                     radius: bottomRadius)
        path.addLine(to: CGPoint(x: rect.minX, y: rect.minY + topRadius))
        path.addArc(tangent1End: CGPoint(x: rect.minX, y: rect.minY),
                     tangent2End: CGPoint(x: rect.minX + topRadius, y: rect.minY),
                     radius: topRadius)
        path.closeSubpath()
        return path
    }
}

struct PulsingDot: View {
    @State private var pulse = false

    var body: some View {
        Circle()
            .fill(.red)
            .frame(width: 6, height: 6)
            .scaleEffect(pulse ? 1.4 : 1.0)
            .opacity(pulse ? 0.5 : 1.0)
            .animation(.easeInOut(duration: 0.6).repeatForever(autoreverses: true), value: pulse)
            .onAppear { pulse = true }
    }
}

struct AudioWaveformView: View {
    @State private var animate = false
    let color: Color

    init(color: Color = .red) {
        self.color = color
    }

    var body: some View {
        HStack(spacing: 2) {
            ForEach(0..<3, id: \.self) { index in
                Capsule()
                    .fill(color)
                    .frame(width: 3, height: animate ? barHeight(for: index) : 4)
                    .animation(
                        .easeInOut(duration: 0.4 + Double(index) * 0.15)
                            .repeatForever(autoreverses: true),
                        value: animate
                    )
            }
        }
        .frame(height: 16)
        .onAppear { animate = true }
    }

    private func barHeight(for index: Int) -> CGFloat {
        switch index {
        case 0: return 12
        case 1: return 16
        case 2: return 10
        default: return 8
        }
    }
}

struct NotchProgressBar: View {
    @State private var offset: CGFloat = -1

    var body: some View {
        GeometryReader { geo in
            Capsule()
                .fill(
                    LinearGradient(
                        colors: [.orange.opacity(0), .orange, .orange.opacity(0)],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: geo.size.width * 0.4, height: 2)
                .offset(x: offset * geo.size.width)
                .onAppear {
                    withAnimation(.easeInOut(duration: 1.2).repeatForever(autoreverses: true)) {
                        offset = 0.6
                    }
                }
        }
        .frame(height: 2)
        .clipped()
    }
}

struct NotchButton: View {
    let title: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(.white)
                .padding(.horizontal, 14)
                .padding(.vertical, 6)
                .background(Capsule().fill(color.opacity(0.85)))
        }
        .buttonStyle(.plain)
    }
}
