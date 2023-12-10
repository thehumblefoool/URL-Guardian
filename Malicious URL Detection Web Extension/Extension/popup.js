document.addEventListener('DOMContentLoaded', function() {
    const currentUrlElement = document.getElementById('currentUrl').querySelector('span');
    const currentUrlResults = document.getElementById('currentUrlResults');
    const userUrlResults = document.getElementById('userUrlResults');
    const urlInput = document.getElementById('urlInput');
    const checkUrlButton = document.getElementById('checkUrlButton');

    //Checks if the input is a valid URL
    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (error) {
            return false;
        }
    }

    //Function to check URL and display model predictions
    function checkURL(url, resultsContainer) {
        //No need to check new/blank tab
        if (!url || url.startsWith("chrome://newtab/") || url.startsWith("chrome-extension://")) {
            resultsContainer.textContent = "No need to check this URL.";
            return;
        }

        // Display a message while checking URL
        resultsContainer.textContent = 'Checking URL...';

        //Send a POST request to the server to check URL
        fetch('http://127.0.0.1:5000/check_url', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            displayResults(data, resultsContainer);
        })
        .catch(error => {
            resultsContainer.textContent = `Error checking URL: ${error.message}`;
            console.error('Error:', error);
        });
    }

    //Function to display model predictions
    function displayResults(data, resultsContainer) {
        resultsContainer.innerHTML = '';
        let isMalicious = false;
        let isBlacklisted = false;
    
        Object.entries(data).forEach(([model, result]) => {
            const resultElement = document.createElement('div');
            resultElement.textContent = `${model} prediction: ${result}`;
            resultsContainer.appendChild(resultElement);
    
            if (result === 'Malicious') {
                isMalicious = true;
            }
            if (result === 'Blacklisted') {
                isBlacklisted = true;
            }
        });
    
        const messageElement = document.createElement('div');
        messageElement.className = (isMalicious || isBlacklisted) ? 'warning-message' : 'safe-message';
        messageElement.textContent = (isMalicious || isBlacklisted) ? 'Warning: This URL may be malicious or blacklisted.' : 'The current URL is safe to browse.';
        resultsContainer.insertBefore(messageElement, resultsContainer.firstChild);
    }

    //Checking the current URL
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        if (tabs.length > 0 && tabs[0].url && isValidUrl(tabs[0].url)) {
            currentUrlElement.textContent = tabs[0].url;
            checkURL(tabs[0].url, currentUrlResults);
        }
    });

    //Check the URL input
    checkUrlButton.addEventListener('click', function() {
        const urlToCheck = urlInput.value;
        if (isValidUrl(urlToCheck)) {
            checkURL(urlToCheck, userUrlResults);
        } else {
            userUrlResults.textContent = 'Invalid input: Please enter a valid URL.';
        }
    });
});
