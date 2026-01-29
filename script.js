import java.util.*;

class BurnoutAnalyzer {

    // ---------- Burnout Risk (simulated ML logic) ----------
    static double burnoutRisk(int work, int sleep) {
        double risk = (work * 7) - (sleep * 5);
        if (risk < 0) risk = 0;
        if (risk > 100) risk = 100;
        return risk;
    }

    // ---------- Stress Level & Suggestions ----------
    static String getStressLevel(int work, int sleep, List<String> suggestions) {

        if (work >= 10 && sleep <= 5) {
            suggestions.add("Reduce working hours");
            suggestions.add("Sleep at least 7 hours");
            suggestions.add("Avoid overtime");
            suggestions.add("Take mental breaks");
            return "High";
        } 
        else if (work >= 8) {
            suggestions.add("Maintain work-life balance");
            suggestions.add("Avoid late nights");
            return "Medium";
        } 
        else {
            suggestions.add("You are following a healthy routine");
            return "Low";
        }
    }

    // ---------- MAIN ----------
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("=== BURNOUT & STRESS ANALYSIS SYSTEM ===");

        System.out.print("Enter Working Hours: ");
        int work = sc.nextInt();

        System.out.print("Enter Sleep Hours: ");
        int sleep = sc.nextInt();

        double risk = burnoutRisk(work, sleep);

        List<String> suggestions = new ArrayList<>();
        String stress = getStressLevel(work, sleep, suggestions);

        System.out.println("\n📊 RESULT");
        System.out.println("Burnout Risk: " + risk + "%");
        System.out.println("Stress Level: " + stress);

        System.out.println("\nSuggestions:");
        for (String s : suggestions) {
            System.out.println("- " + s);
        }

        sc.close();
    }
}
