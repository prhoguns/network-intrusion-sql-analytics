# Findings

The three selected days yield **2,428,245 valid flows**: 1,668,042 benign and 760,203 labeled attack flows. This is a scenario-selected corpus, so the 31.31% attack share is **not** an estimate of real-world traffic prevalence. [Class mix](results/01_attack_mix.md)

1. **Attack classes align strongly with particular destination ports in these scenarios.** Port 8080 has 281,660 labeled attacks, port 21 has 193,419, and port 22 has 188,319. This reflects the dataset's scripted scenarios and should not become a universal port blocklist. [Port table](results/05_attacked_ports.md)
2. **The three days contribute distinct attack classes:** `FTP-BruteForce`, `SSH-Bruteforce`, `Infilteration`, and `Bot`. The exact source spelling of `Infilteration` is retained. [Daily mix](results/02_daily_mix.md)
3. **A naive short-SYN rule performs poorly across this mixed corpus.** It produces 66,060 alerts, finds 4,607 labeled attacks, and reaches only 6.97% precision and 0.61% recall. This is a useful baseline demonstrating why traffic context matters. [Rule result](results/17_simple_flag_tradeoff.md)

## Limits

Only three of the source release's days are included. The labels are scenario labels from a generated test environment; cross-day class proportions are not a population estimate. The rule evaluation is descriptive on the same data used to choose the rule. The source CSVs include repeated header lines, which the build script excludes.
