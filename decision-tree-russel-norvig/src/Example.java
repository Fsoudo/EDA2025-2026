package src;

import java.util.EnumMap;
import java.util.Map;

/**
 * One training example from the R&N restaurant dataset.
 */
public class Example {

    private final int              id;
    private final Map<Attribute, String> attrs;
    private final boolean          willWait;

    public Example(int id, boolean willWait,
                   String alternate, String bar, String friSat,
                   String hungry, String patrons, String price,
                   String raining, String reservation,
                   String type, String waitEst) {

        this.id       = id;
        this.willWait = willWait;
        this.attrs    = new EnumMap<>(Attribute.class);

        this.attrs.put(Attribute.ALTERNATE,   alternate);
        this.attrs.put(Attribute.BAR,         bar);
        this.attrs.put(Attribute.FRI_SAT,     friSat);
        this.attrs.put(Attribute.HUNGRY,      hungry);
        this.attrs.put(Attribute.PATRONS,     patrons);
        this.attrs.put(Attribute.PRICE,       price);
        this.attrs.put(Attribute.RAINING,     raining);
        this.attrs.put(Attribute.RESERVATION, reservation);
        this.attrs.put(Attribute.TYPE,        type);
        this.attrs.put(Attribute.WAIT_EST,    waitEst);
    }

    public int       getId()                          { return this.id;              }
    public boolean   isWillWait()                     { return this.willWait;        }
    public String    getValue(Attribute attr)          { return this.attrs.get(attr); }

    @Override
    public String toString() {
        return "E" + this.id + "(" + (this.willWait ? "YES" : "NO") + ")";
    }
}
