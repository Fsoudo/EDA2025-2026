package src;

/**
 * Attributes from Russell & Norvig restaurant waiting problem (Fig 18.3).
 */
public enum Attribute {
    ALTERNATE   ("Alternate",    "yes", "no"),
    BAR         ("Bar",          "yes", "no"),
    FRI_SAT     ("Fri/Sat",      "yes", "no"),
    HUNGRY      ("Hungry",       "yes", "no"),
    PATRONS     ("Patrons",      "None", "Some", "Full"),
    PRICE       ("Price",        "$", "$$", "$$$"),
    RAINING     ("Raining",      "yes", "no"),
    RESERVATION ("Reservation",  "yes", "no"),
    TYPE        ("Type",         "French", "Thai", "Burger", "Italian"),
    WAIT_EST    ("WaitEstimate", "0-10", "10-30", "30-60", ">60");

    private final String name;
    private final String[] values;

    Attribute(String name, String... values) {
        this.name   = name;
        this.values = values;
    }

    public String getName()     { return this.name;   }
    public String[] getValues() { return this.values; }
}
