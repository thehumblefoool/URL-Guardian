chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.url) {
        if (isEmptyOrNewTab(changeInfo.url)) {
            clearMaliciousUrlBadge(tabId);
        } else {
            checkURL(changeInfo.url, tabId, (isMalicious) => {
                if (isMalicious) {
                    showMaliciousUrlBadge(tabId);
                    WarningBanner(tabId);
                } else {
                    clearMaliciousUrlBadge(tabId);
                }
            });
        }
    }
});

//Function to check empty or new tab
function isEmptyOrNewTab(url) {
    return !url || url.startsWith("chrome://newtab/") || url.startsWith("chrome-extension://");
}

//Function to check the URL
function checkURL(url, tabId, callback) {
    fetch('http://127.0.0.1:5000/check_url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        //Checks if any model predicted the URL as malicious
        let isMalicious = Object.values(data).some(result => result === 'Malicious');
        callback(isMalicious);
    })
    .catch(error => {
        console.error('Error checking URL:', error);
    });
}

//function to display a malicious badge
function showMaliciousUrlBadge(tabId) {
    chrome.action.setBadgeBackgroundColor({ tabId: tabId, color: '#FF0000' });
    chrome.action.setBadgeText({ tabId: tabId, text: '!' });
}

//Function to clear malicious badge
function clearMaliciousUrlBadge(tabId) {
    chrome.action.setBadgeText({ tabId: tabId, text: '' });
}

//Function to display a warning banner
function WarningBanner(tabId) {
    chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: () => {
            const banner = document.createElement('div');
            banner.style.position = 'fixed';
            banner.style.width = '100%';
            banner.style.backgroundColor = 'red';
            banner.style.color = 'white';
            banner.style.zIndex = '10000';
            banner.style.textAlign = 'center';
            banner.style.padding = '10px';
            banner.textContent = 'Warning: This URL may be malicious!';
            document.body.prepend(banner);
        }
    });
}
