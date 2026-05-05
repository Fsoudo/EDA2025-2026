package src;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Decision Tree Learning (ID3 / DTL) — Russell & Norvig.
 *
 * Every recursive call prints its full state so the user can
 * trace the algorithm step by step in the console.
 */
public class DTL {

    // ── ANSI colour codes ──────────────────────────────────────────────────
    private static final String RESET  = "\u001B[0m";
    private static final String BOLD   = "\u001B[1m";
    private static final String CYAN   = "\u001B[36m";
    private static final String GREEN  = "\u001B[32m";
    private static final String YELLOW = "\u001B[33m";
    private static final String RED    = "\u001B[31m";
    private static final String BLUE   = "\u001B[34m";
    private static final String PURPLE = "\u001B[35m";

    private int stepCount = 0;

    // ══════════════════════════════════════════════════════════════════════
    //  PUBLIC ENTRY
    // ══════════════════════════════════════════════════════════════════════

    /**
     * Learn a decision tree from examples using DTL (ID3).
     *
     * @param examples       current training subset
     * @param attributes     remaining candidate attributes
     * @param parentExamples examples from parent call (for plurality fallback)
     * @param depth          recursion depth (for indentation)
     * @return learned TreeNode
     */
    public TreeNode learn(List<Example> examples,
                          List<Attribute> attributes,
                          List<Example> parentExamples,
                          int depth) {

        this.stepCount++;
        String indent = "  ".repeat(depth);
        printStepHeader(depth, this.stepCount, examples, attributes);

        // ── BASE CASE 1: no examples → plurality of parent ─────────────────
        if (examples.isEmpty()) {
            boolean plurality = plurality(parentExamples);
            printAction(indent, RED, "BASE CASE — examples empty → PLURALITY(parent) = " + label(plurality));
            printSeparator(depth);
            return new LeafNode(plurality);
        }

        // ── BASE CASE 2: all same class ────────────────────────────────────
        if (allSameClass(examples)) {
            boolean cls = examples.get(0).isWillWait();
            printAction(indent, GREEN, "BASE CASE — all same class → Leaf(" + label(cls) + ")");
            printSeparator(depth);
            return new LeafNode(cls);
        }

        // ── BASE CASE 3: no attributes left ───────────────────────────────
        if (attributes.isEmpty()) {
            boolean plurality = plurality(examples);
            printAction(indent, YELLOW, "BASE CASE — no attributes → PLURALITY = " + label(plurality));
            printSeparator(depth);
            return new LeafNode(plurality);
        }

        // ── COMPUTE INFORMATION GAIN for each attribute ───────────────────
        double parentEntropy = entropy(examples);
        Map<Attribute, Double> gains = computeGains(examples, attributes, parentEntropy);
        printEntropyAndGains(indent, parentEntropy, gains, examples);

        // ── CHOOSE BEST ATTRIBUTE ─────────────────────────────────────────
        Attribute best = bestAttribute(gains);
        printAction(indent, CYAN, "SPLIT on " + BOLD + best.getName() + RESET + CYAN
                + "  (gain = " + String.format("%.4f", gains.get(best)) + " bits)");

        // ── RECURSE on each branch ────────────────────────────────────────
        DecisionNode node = new DecisionNode(best);
        List<Attribute> remaining = new ArrayList<>(attributes);
        remaining.remove(best);

        for (String value : best.getValues()) {
            List<Example> subset = filterByValue(examples, best, value);
            printBranchInfo(indent, best.getName(), value, subset);
            TreeNode subtree = learn(subset, remaining, examples, depth + 1);
            node.addBranch(value, subtree);
        }

        printSeparator(depth);
        return node;
    }

    // ══════════════════════════════════════════════════════════════════════
    //  INFORMATION THEORY
    // ══════════════════════════════════════════════════════════════════════

    /** Shannon entropy H(examples) in bits. */
    private double entropy(List<Example> examples) {
        if (examples.isEmpty()) return 0.0;
        long pos   = examples.stream().filter(Example::isWillWait).count();
        long neg   = examples.size() - pos;
        return entropyBits(pos, neg, examples.size());
    }

    private double entropyBits(long pos, long neg, long total) {
        if (total == 0 || pos == 0 || neg == 0) return 0.0;
        double p = (double) pos / total;
        double n = (double) neg / total;
        return -p * log2(p) - n * log2(n);
    }

    private double log2(double x) { return Math.log(x) / Math.log(2); }

    /** Information gain: H(parent) − remainder(attr, examples). */
    private double informationGain(List<Example> examples, Attribute attr, double parentEntropy) {
        double remainder = 0.0;
        for (String value : attr.getValues()) {
            List<Example> subset = filterByValue(examples, attr, value);
            if (!subset.isEmpty()) {
                remainder += ((double) subset.size() / examples.size()) * entropy(subset);
            }
        }
        return parentEntropy - remainder;
    }

    private Map<Attribute, Double> computeGains(List<Example> examples,
                                                 List<Attribute> attributes,
                                                 double parentEntropy) {
        Map<Attribute, Double> gains = new LinkedHashMap<>();
        for (Attribute attr : attributes) {
            gains.put(attr, informationGain(examples, attr, parentEntropy));
        }
        return gains;
    }

    // ══════════════════════════════════════════════════════════════════════
    //  UTILITY
    // ══════════════════════════════════════════════════════════════════════

    private boolean allSameClass(List<Example> examples) {
        boolean first = examples.get(0).isWillWait();
        return examples.stream().allMatch(e -> e.isWillWait() == first);
    }

    /** Most common class; ties broken toward true (yes). */
    private boolean plurality(List<Example> examples) {
        long pos = examples.stream().filter(Example::isWillWait).count();
        return pos >= examples.size() - pos;
    }

    private Attribute bestAttribute(Map<Attribute, Double> gains) {
        return gains.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .orElseThrow()
                .getKey();
    }

    private List<Example> filterByValue(List<Example> examples, Attribute attr, String value) {
        return examples.stream()
                .filter(e -> value.equals(e.getValue(attr)))
                .collect(Collectors.toList());
    }

    private String label(boolean b) { return b ? "YES" : "NO"; }

    // ══════════════════════════════════════════════════════════════════════
    //  PRINTING — visible algorithm states
    // ══════════════════════════════════════════════════════════════════════

    private void printStepHeader(int depth, int step, List<Example> examples, List<Attribute> attrs) {
        String indent = "  ".repeat(depth);
        long pos = examples.stream().filter(Example::isWillWait).count();
        long neg = examples.size() - pos;

        String exIds = examples.stream()
                .map(e -> "E" + e.getId())
                .collect(Collectors.joining(", "));

        String attrNames = attrs.stream()
                .map(Attribute::getName)
                .collect(Collectors.joining(", "));

        System.out.println();
        System.out.println(indent + BOLD + BLUE + "┌─ STEP " + step + "  depth=" + depth + RESET);
        System.out.println(indent + BLUE + "│  Examples [" + examples.size() + "] " + RESET
                + GREEN + "YES=" + pos + RESET + "  " + RED + "NO=" + neg + RESET
                + "  →  " + exIds);
        System.out.println(indent + BLUE + "│  Attributes: " + RESET + attrNames);
        System.out.println(indent + BLUE + "│" + RESET);
    }

    private void printEntropyAndGains(String indent,
                                       double parentEntropy,
                                       Map<Attribute, Double> gains,
                                       List<Example> examples) {
        // find best for highlighting
        Attribute best = bestAttribute(gains);

        System.out.println(indent + BLUE + "│  " + RESET
                + YELLOW + "H(examples) = " + String.format("%.4f", parentEntropy) + " bits" + RESET);
        System.out.println(indent + BLUE + "│" + RESET);
        System.out.printf(indent + BLUE + "│  " + RESET + PURPLE + "%-16s  %-7s  %s%n" + RESET,
                "Attribute", "Gain", "Partition sizes");

        for (Map.Entry<Attribute, Double> entry : gains.entrySet()) {
            Attribute attr  = entry.getKey();
            double    gain  = entry.getValue();

            StringBuilder partitions = new StringBuilder();
            for (String val : attr.getValues()) {
                int sz = filterByValue(examples, attr, val).size();
                if (sz > 0) partitions.append(val).append("=").append(sz).append("  ");
            }

            boolean isBest = attr == best;
            String colour  = isBest ? (BOLD + CYAN) : "";
            String marker  = isBest ? " ◄ BEST" : "";
            System.out.printf(indent + BLUE + "│  " + RESET + colour + "%-16s  %-7s  %s%s%n" + RESET,
                    attr.getName(),
                    String.format("%.4f", gain),
                    partitions.toString().trim(),
                    marker);
        }
        System.out.println(indent + BLUE + "│" + RESET);
    }

    private void printAction(String indent, String colour, String message) {
        System.out.println(indent + BLUE + "│  " + RESET + colour + "→ " + message + RESET);
    }

    private void printBranchInfo(String indent, String attrName, String value, List<Example> subset) {
        String exIds = subset.isEmpty()
                ? "(none)"
                : subset.stream().map(e -> "E" + e.getId()).collect(Collectors.joining(", "));
        System.out.println(indent + BLUE + "│  " + RESET
                + YELLOW + "Branch " + attrName + "=" + value
                + RESET + "  size=" + subset.size() + "  " + exIds);
    }

    private void printSeparator(int depth) {
        System.out.println("  ".repeat(depth) + BLUE + "└" + "─".repeat(50) + RESET);
    }
}
