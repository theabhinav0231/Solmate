function selectOption(option) {
    // Deselect all options
    document.querySelectorAll(".option").forEach(opt => {
        opt.classList.remove("selected");
        opt.querySelector("input").checked = false;
        opt.style.transform = "scale(1)"; // Reset scale effect
    });

    // Select the clicked option
    option.classList.add("selected");
    option.querySelector("input").checked = true;

    // Add a smooth scale effect on selection
    option.style.transition = "transform 0.2s ease-in-out";
    option.style.transform = "scale(1.05)";

    // Enable the Next button with animation
    let nextBtn = document.getElementById("nextBtn");
    if (nextBtn) {
        nextBtn.classList.add("active");
        nextBtn.disabled = false;
        nextBtn.style.transition = "background 0.3s ease-in-out, transform 0.2s";
        nextBtn.style.transform = "scale(1.1)";
        
        // Slightly scale back the button after effect
        setTimeout(() => nextBtn.style.transform = "scale(1)", 200);
    }
}
