document.addEventListener('DOMContentLoaded', () => {
    const journalForm = document.getElementById('journal-form');
    const journalEntry = document.getElementById('journal-entry');
    const historyDropdown = document.getElementById('history-dropdown');

    journalForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const entryText = journalEntry.value.trim();

        if (entryText) {
            const data = {
                timestamp: new Date().toISOString(),
                entry: entryText
            };

            console.log("Submitting:", data);

            alert("Your feelings have been logged.");
            journalEntry.value = "";
        } else {
            alert("Please write something before submitting.");
        }
    });

    historyDropdown.addEventListener('change', (event) => {
        const selectedPeriod = event.target.value;
        console.log("Request summary:", selectedPeriod);
        alert(`Requesting summary for: ${selectedPeriod}`);
    });
});
