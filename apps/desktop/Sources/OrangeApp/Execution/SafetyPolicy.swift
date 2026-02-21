import Foundation

enum SafetyCategory: String, Codable, CaseIterable {
    case none
    case send
    case delete
    case purchase
    case externalPost = "external_post"
    case script
}

enum SafetyApprovalMode: String, Codable, CaseIterable {
    case oneTime = "one_time"
    case perSession = "per_session"
    case alwaysAsk = "always_ask"
}

struct SafetyPrompt: Identifiable {
    let id = UUID()
    let category: SafetyCategory
    let approvalMode: SafetyApprovalMode
    let title: String
    let message: String
}

protocol SafetyPolicy {
    func evaluate(actions: [AgentAction]) -> [SafetyPrompt]
    func category(for action: AgentAction) -> SafetyCategory
}

struct DefaultSafetyPolicy: SafetyPolicy {
    func evaluate(actions: [AgentAction]) -> [SafetyPrompt] {
        var prompts: [SafetyPrompt] = []
        var seen = Set<SafetyCategory>()

        for action in actions {
            let category = category(for: action)
            guard category != .none else { continue }
            guard !seen.contains(category) else { continue }
            seen.insert(category)
            prompts.append(prompt(for: category))
        }

        return prompts
    }

    func category(for action: AgentAction) -> SafetyCategory {
        if action.kind == .runAppleScript {
            return .script
        }

        let joined = [action.target, action.text, action.expectedOutcome]
            .compactMap { $0?.lowercased() }
            .joined(separator: " ")

        if containsAny(["delete", "remove", "trash", "erase"], in: joined) || action.destructive {
            return .delete
        }
        if containsAny(["purchase", "buy", "checkout", "payment", "pay"], in: joined) {
            return .purchase
        }
        if containsAny(["post", "tweet", "publish", "share externally", "external"], in: joined) {
            return .externalPost
        }
        if containsAny(["send", "submit", "reply", "message"], in: joined) {
            return .send
        }
        return .none
    }

    private func prompt(for category: SafetyCategory) -> SafetyPrompt {
        let mode = approvalMode(for: category)
        switch category {
        case .none:
            return SafetyPrompt(
                category: .none,
                approvalMode: mode,
                title: "No Confirmation Needed",
                message: "This action is safe to run."
            )
        case .send:
            return SafetyPrompt(
                category: .send,
                approvalMode: mode,
                title: "Confirm Send Action",
                message: "Orange will send or submit content. Approval required."
            )
        case .delete:
            return SafetyPrompt(
                category: .delete,
                approvalMode: mode,
                title: "Confirm Delete Action",
                message: "Orange will delete or remove content. Approval required."
            )
        case .purchase:
            return SafetyPrompt(
                category: .purchase,
                approvalMode: mode,
                title: "Confirm Purchase Action",
                message: "Orange may complete a purchase or payment. Approval required."
            )
        case .externalPost:
            return SafetyPrompt(
                category: .externalPost,
                approvalMode: mode,
                title: "Confirm External Post",
                message: "Orange will post externally. Approval required."
            )
        case .script:
            return SafetyPrompt(
                category: .script,
                approvalMode: mode,
                title: "Confirm Script Execution",
                message: "Generated AppleScript will run. Explicit approval required."
            )
        }
    }

    private func approvalMode(for category: SafetyCategory) -> SafetyApprovalMode {
        let key = "safety.approval_mode.\(category.rawValue)"
        let stored = UserDefaults.standard.string(forKey: key) ?? SafetyApprovalMode.alwaysAsk.rawValue
        return SafetyApprovalMode(rawValue: stored) ?? .alwaysAsk
    }

    private func containsAny(_ terms: [String], in text: String) -> Bool {
        terms.contains(where: { text.contains($0) })
    }
}
