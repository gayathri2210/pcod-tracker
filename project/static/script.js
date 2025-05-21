// project/static/script.js (EXTREMELY SIMPLIFIED TEST)

alert("SCRIPT.JS IS LOADED AND RUNNING!"); // First test: Is this file even parsed?

console.log("[SCRIPT.JS] TOP LEVEL: This is a console log from the simplified script.js.");

document.addEventListener('DOMContentLoaded', () => {
    console.log("[SCRIPT.JS] DOMContentLoaded event fired from simplified script.");
    
    const pcosForm = document.getElementById('pcosForm'); // Attempt to find the form

    if (pcosForm) {
        console.log("[SCRIPT.JS] Simplified: HTML Element with ID 'pcosForm' was FOUND.");
        
        pcosForm.addEventListener('submit', function(event) {
            console.log("[SCRIPT.JS] Simplified: PCOS Form 'submit' event TRIGGERED.");
            
            alert("Simplified Script: Submit event TRIGGERED! Attempting to prevent default browser action."); // Test alert
            
            event.preventDefault(); // THE KEY LINE
            
            console.log("[SCRIPT.JS] Simplified: Default form submission should have been PREVENTED by JavaScript.");
            alert("Simplified Script: Default submission should be prevented. If page reloaded, it FAILED.");
            
            // Intentionally do nothing else here (no fetch, no UI updates)
            // We only want to test if preventDefault works.
            // If it works, the page should NOT reload, and your Flask terminal
            // should NOT show a new GET /index?... request.
        });
        console.log("[SCRIPT.JS] Simplified: 'submit' event listener has been ATTACHED to pcosForm.");

    } else {
        console.error("[SCRIPT.JS] Simplified: CRITICAL - HTML Element with ID 'pcosForm' was NOT FOUND!");
        alert("Simplified Script CRITICAL ERROR: HTML form with ID 'pcosForm' NOT FOUND on this page!");
    }
});

console.log("[SCRIPT.JS] BOTTOM LEVEL: Simplified script.js parsing complete.");

