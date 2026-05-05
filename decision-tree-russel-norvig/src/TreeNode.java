package src;

/**
 * Abstract base for decision tree nodes.
 */
public abstract class TreeNode {
    public abstract boolean isLeaf();
    public abstract boolean classify(Example e);
    public abstract String display(String indent);

    @Override
    public String toString() { return display(""); }
}
