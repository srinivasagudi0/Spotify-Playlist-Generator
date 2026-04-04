const form = document.querySelector(".composer-form");
const moodInput = document.querySelector('textarea[name="mood_text"]');
const marketInput = document.querySelector('input[name="market"]');
const limitInput = document.getElementById("limit");
const limitValue = document.getElementById("limitValue");
const loadingNote = document.querySelector("[data-loading-note]");
const exampleButtons = document.querySelectorAll("[data-fill]");

if (limitInput && limitValue) {
    const syncLimit = () => {
        limitValue.textContent = limitInput.value;
    };

    limitInput.addEventListener("input", syncLimit);
    syncLimit();
}

if (moodInput) {
    const autoResize = () => {
        moodInput.style.height = "auto";
        moodInput.style.height = `${Math.max(moodInput.scrollHeight, 150)}px`;
    };

    moodInput.addEventListener("input", autoResize);
    autoResize();

    exampleButtons.forEach((button) => {
        button.addEventListener("click", () => {
            moodInput.value = button.dataset.fill || "";
            autoResize();
            moodInput.focus();
            moodInput.setSelectionRange(moodInput.value.length, moodInput.value.length);
        });
    });
}

if (marketInput) {
    const normalizeMarket = () => {
        marketInput.value = marketInput.value.replace(/[^a-z]/gi, "").slice(0, 2).toUpperCase();
    };

    marketInput.addEventListener("input", normalizeMarket);
    normalizeMarket();
}

if (form) {
    form.addEventListener("submit", (event) => {
        const submitter = event.submitter;
        const buttons = form.querySelectorAll('button[type="submit"]');
        document.body.classList.add("is-loading");

        buttons.forEach((button) => {
            button.disabled = true;
        });

        if (loadingNote) {
            loadingNote.hidden = false;
            loadingNote.textContent = submitter && submitter.value === "check-config"
                ? "Checking your setup..."
                : "Finding tracks that fit...";
        }

        if (submitter) {
            submitter.textContent = submitter.value === "check-config"
                ? "Checking..."
                : "Building...";
        }
    });
}
