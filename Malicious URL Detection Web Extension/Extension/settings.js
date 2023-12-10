document.addEventListener('DOMContentLoaded', function() {
    const whitelistInput = document.getElementById('whitelistInput');
    const addToWhitelist = document.getElementById('addToWhitelist');
    const removeFromWhitelist = document.getElementById('removeFromWhitelist');
    const blacklistInput = document.getElementById('blacklistInput');
    const addToBlacklist = document.getElementById('addToBlacklist');
    const removeFromBlacklist = document.getElementById('removeFromBlacklist');
    const whitelist = document.getElementById('whitelist');
    const blacklist = document.getElementById('blacklist');

    //Load whitelist/blacklist
    loadLists();

    //Add/remove from whitelist when clicked
    addToWhitelist.addEventListener('click', function() {
        updateList('whitelist', whitelistInput.value.trim(), true);
    });
    removeFromWhitelist.addEventListener('click', function() {
        updateList('whitelist', whitelistInput.value.trim(), false);
    });

    //Add/remove from blacklist when clicked
    addToBlacklist.addEventListener('click', function() {
        updateList('blacklist', blacklistInput.value.trim(), true);
    });
    removeFromBlacklist.addEventListener('click', function() {
        updateList('blacklist', blacklistInput.value.trim(), false);
    });

    //Function to update the whitelist/blacklist
    function updateList(listType, url, add) {
        // Checks if the input is a valid URL 
        if (!url || !isValidUrl(url)) {
            alert('Please enter a valid URL or domain.');
            return;
        }

        //Send a POST request to the server to update the list
        fetch(`http://127.0.0.1:5000/update_${listType}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ url: url, add: add })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadLists(); //Reload list
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating list.');
        });
    }

    //Checks if the input is a valid URL
    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (error) {
            return false;
        }
    }

    //Function to load and display whitelist/blacklist
    function loadLists() {
        fetch('http://127.0.0.1:5000/get_lists')
        .then(response => response.json())
        .then(data => {
            displayList(whitelist, data.whitelist);
            displayList(blacklist, data.blacklist);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading lists.');
        });
    }

    //Function to display whitelisted/blacklisted domains
    function displayList(listElement, urls) {
        listElement.innerHTML = '';
        urls.forEach(url => {
            const listItem = document.createElement('li');
            listItem.textContent = url;
            listElement.appendChild(listItem);
        });
    }
});
