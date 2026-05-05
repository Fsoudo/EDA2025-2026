package src;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Internal decision node: splits on an attribute.
 */
public class DecisionNode extends TreeNode {

    private final Attribute                attribute;
    private final Map<String, TreeNode>    branches;   // value → subtree

    public DecisionNode(Attribute attribute) {
        this.attribute = attribute;
        this.branches  = new LinkedHashMap<>();
    }

    public void addBranch(String value, TreeNode subtree) {
        this.branches.put(value, subtree);
    }

    @Override public boolean isLeaf() { return false; }

    @Override
    public boolean classify(Example e) {
        String value = e.getValue(this.attribute);
        TreeNode branch = this.branches.get(value);
        if (branch == null) throw new IllegalArgumentException("Unknown value: " + value);
        return branch.classify(e);
    }

    @Override
    public String display(String indent) {
        StringBuilder sb = new StringBuilder();
        sb.append(indent).append("[").append(this.attribute.getName()).append("?]");
        for (Map.Entry<String, TreeNode> entry : this.branches.entrySet()) {
            sb.append("\n").append(indent).append("  ├─ ").append(entry.getKey()).append(":");
            sb.append("\n").append(entry.getValue().display(indent + "  │   "));
        }
        return sb.toString();
    }

    public Attribute getAttribute()           { return this.attribute; }
    public Map<String, TreeNode> getBranches() { return this.branches; }
}
