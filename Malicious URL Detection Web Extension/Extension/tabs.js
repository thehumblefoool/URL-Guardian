function switchToCurrentUrlTab() {
    currentUrlTab.classList.add('active');
    userInputTab.classList.remove('active');
    settingsTab.classList.remove('active');
    currentUrlSection.classList.add('active');
    userInputSection.classList.remove('active');
    settingsSection.classList.remove('active');
}

function switchToUserInputTab() {
    userInputTab.classList.add('active');
    currentUrlTab.classList.remove('active');
    settingsTab.classList.remove('active');
    userInputSection.classList.add('active');
    currentUrlSection.classList.remove('active');
    settingsSection.classList.remove('active');
}

function switchToSettingsTab() {
    settingsTab.classList.add('active');
    currentUrlTab.classList.remove('active');
    userInputTab.classList.remove('active');
    settingsSection.classList.add('active');
    currentUrlSection.classList.remove('active');
    userInputSection.classList.remove('active');
}

//Default tab
switchToCurrentUrlTab();

currentUrlTab.addEventListener('click', switchToCurrentUrlTab);
userInputTab.addEventListener('click', switchToUserInputTab);
settingsTab.addEventListener('click', switchToSettingsTab);
