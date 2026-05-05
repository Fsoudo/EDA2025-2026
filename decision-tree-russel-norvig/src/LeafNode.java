package src;

/**
 * Leaf node: stores final classification (true = WillWait).
 */
public class LeafNode extends TreeNode {

    private final boolean classification;

    public LeafNode(boolean classification) {
        this.classification = classification;
    }

    @Override public boolean isLeaf()           { return true;                }
    @Override public boolean classify(Example e) { return this.classification; }

    @Override
    public String display(String indent) {
        String label = this.classification ? "YES" : "NO";
        return indent + "[Leaf: " + label + "]";
    }
}
