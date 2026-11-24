# How to Check OCG 1103 Old Rulings in 3 Steps

In **Yu-Gi-Oh! OCG 1103** (March 2011 banlist, Master Rule 2), many card texts and rulings have changed over the years. Modern databases, default YGOPro scripts, and even the **current page** of `yugioh-wiki.net` often reflect newer rulings or have removed old Q&As.

You do not need any scripts or AI tools to verify a 2011 ruling—just follow these three steps.

---

## Step 1: Confirm the Exact Japanese Card Name & 2011 Card Text

1. **Get the exact Japanese name**: Look up the card in a database (such as Yugipedia or ygocdb) and copy its exact Japanese name. Even one wrong kana or punctuation mark will return 404 on Japanese wikis.
2. **Check for errata**:
   - Search the card on `yugioh-wiki.net`'s [Errata page (エラッタ)](https://yugioh-wiki.net/index.php?%A5%A8%A5%E9%A5%C3%A5%BF).
   - Watch out for the **July 10, 2014 batch errata (279 cards)**, which changed *"until the End Phase"* (`エンドフェイズ時まで`, expiring as a separate step during the End Phase) to *"until the end of this turn"* (`ターン終了時まで`).
   - To inspect exact historical Japanese wordings by set, open `https://yugipedia.com/wiki/Card_Errata:<English_Card_Name>` and check the **Japanese** section for printings released on or before **August 31, 2011**.

---

## Step 2: Check `yugioh-wiki.net` Backup Revisions (Not the Current Page)

The current page on `yugioh-wiki.net` frequently removes or rewrites obsolete Q&As (for example, the old ruling for *Cup of Ace* has been deleted from its current page). Always use **Backup (バックアップ)** revisions:

1. Open the card's page on `yugioh-wiki.net` and click **バックアップ** (Backup) in the page navigation.
   - The list URL looks like: `https://yugioh-wiki.net/index.php?cmd=backup&page=<EUC-JP card name>`
   - Each revision is listed as `N (YYYY/MM/DD HH:MM:SS)`.
2. **Separate the ruling date from the archive date**:
   - **Determine the ruling (by Q&A date)**: Look for the latest `Ｑ： / Ａ： ... (YY/MM/DD)` entry dated **on or before `2011-09-01`**.
     - Only use a ruling dated after `2011-09-01` if no earlier ruling exists, and clearly label it as a *post-cutoff exception*.
   - **Pick the link (by archive revision)**: Open the **earliest backup revision (`&age=N`)** that contains that Q&A. Many cards have no 2011 backup snapshot at all (e.g., their first snapshot is from 2012 or 2015)—that is fine as long as the Q&A date inside that snapshot is on or before `2011-09-01`.
3. When citing, record all three: **snapshot date, `&age=N` URL, and Q&A date** (e.g., `wiki Elemental HERO Nova Master 2011-01-10 snapshot (age=42), Q&A (11/01/09)`).

---

## Step 3: Cross-Check Kanpatei's 1103 Compilation & Label Evidence Grade

1. Open Kanpatei's [1103 Major Card Rulings Compilation (1103環境 主要カード 裁定まとめ)](https://note.com/sabae5280/n/n95ba4b085cf6) and search (`Ctrl+F`) for the Japanese card name.
   - Kanpatei is a major Japanese 1103 tournament series. Its compilation targets Master Rule 2 / 1103 specifically and includes a Damage Step timing chart, filling gaps where `yugioh-wiki` is missing or ambiguous.
   - If an entry says `当時調整中` ("under adjustment at the time") or cites a later answer (e.g., `14/02 回答`), note that faithfully.
2. **State the evidence grade clearly when sharing your conclusion**:
   - **Direct ruling**: Explicit Q&A for the card itself, with `&age=N` link or Kanpatei entry.
   - **Analogy**: Explicit ruling for another card with identical wording and conditions (note that the card itself has no direct Q&A).
   - **Indirect**: Inferred from 2011 card text or Master Rule 2 without an explicit Q&A (mark as unconfirmed).
   - **Post-cutoff exception**: No ruling before `2011-09-01`; using the closest ruling after the cutoff (state the date).
   - **No source found**: Say so plainly instead of citing a modern page or guessing.

---

## Using This Method for Other OCG Eras

To check another OCG historical format (e.g., 2004, 2008, 2012):

- Replace the `2011-09-01` cutoff in Step 2 with your target format's end date.
- **Keep in mind**: Non-1103 OCG eras usually do not have a curated community compilation comparable to Kanpatei. You will have to rely primarily on `yugioh-wiki.net` historical revisions and general rules, so expect lower evidence grades on edge cases and label them accordingly.
