package src;

import java.util.Arrays;
import java.util.List;

/**
 * Hardcoded R&N restaurant dataset — Fig 18.3 (12 examples).
 *
 * Column order: Alt, Bar, Fri, Hun, Patrons, Price, Rain, Res, Type, WaitEst, WillWait
 */
public class Dataset {

    private Dataset() {}

    public static List<Example> load() {
        return Arrays.asList(
            new Example( 1, true,  "yes","no", "no", "yes","Some","$$$","no", "yes","French", "0-10"),
            new Example( 2, false, "yes","no", "no", "yes","Full","$",  "no", "no", "Thai",   "30-60"),
            new Example( 3, true,  "no", "yes","no", "no", "Some","$",  "no", "no", "Burger", "0-10"),
            new Example( 4, true,  "yes","no", "yes","yes","Full","$",  "yes","no", "Thai",   "10-30"),
            new Example( 5, false, "yes","no", "yes","no", "Full","$$$","no", "yes","French", ">60"),
            new Example( 6, true,  "no", "yes","no", "yes","Some","$$", "yes","yes","Italian","0-10"),
            new Example( 7, false, "no", "yes","no", "no", "None","$",  "yes","no", "Burger", "0-10"),
            new Example( 8, true,  "no", "no", "no", "yes","Some","$$", "yes","yes","Thai",   "0-10"),
            new Example( 9, false, "yes","yes","no", "no", "Full","$",  "yes","no", "Burger", ">60"),
            new Example(10, false, "yes","no", "yes","yes","Full","$$$","no", "yes","Italian","10-30"),
            new Example(11, false, "no", "no", "no", "no", "None","$",  "no", "no", "Thai",   "0-10"),
            new Example(12, true,  "yes","yes","yes","yes","Full","$",  "no", "no", "Burger", "30-60")
        );
    }
}
