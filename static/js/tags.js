//Declare tagify variables
export var jobTagify, softwareTagify;

/*DO NOT USE JQUERY WITH TAGIFY */
var jobWhitelist = getJobWhitelist();
var softwareWhitelist = getSoftwareWhitelist();

//Find user input in job class question
var jobInput = document.querySelector("input[id=job-type-text-input]");
jobTagify = new Tagify (jobInput, {
    enforceWhitelist: true,
    whitelist: [],
    skipInvalid: true,
    keepInvalidTags: false,
    editTags: false,
    dropdown: {
        maxItems: 5,
        enabled: 0
    }
})

//Find user input in software question
var softwareInput = document.querySelector("input[id=software-text-input]");
softwareTagify = new Tagify (softwareInput, {
    enforceWhitelist: true,
    whitelist: [],
    skipInvalid: true,
    keepInvalidTags: false,
    editTags: false,
    dropdown: {
        maxItems: 5,
        enabled: 0
    }
});

// grab whitelist for job class tags from AJAX
async function getJobWhitelist(userInput){
    //if user hasn't type anything or erased their input, whitelist is populated with all possible job classes
    if (userInput === undefined || userInput.length < 1){
        return await $.ajax({
            type: "GET",
            url: "/get_job_classes"
        });
    }else{ //otherwise, whitelist is only populated with job classes containing their input as a substring
        return await $.ajax({
            type: "GET",
            url: "/get_job_classes/" + userInput
        });
    }
}

// grab whitelist for software tags from AJAX
async function getSoftwareWhitelist(userInput){
    //if user hasn't type anything or erased their input, whitelist is populated with all possible job classes
    if (userInput === undefined || userInput.length < 1){
        return await $.ajax({
            type: "GET",
            url: "/get_software"
        });
    }else{
        return await $.ajax({
            type: "GET",
            url: "/get_software/" + userInput
        })
    }
}

export async function jobTagInput(e){
    // clear current whitelist
	jobTagify.settings.whitelist.length = 0; // reset current whitelist
	// show loader & hide suggestions dropdown (if opened)
    jobTagify.loading(true).dropdown.hide.call(jobTagify)

    var userInput = e.detail.value;
    console.log("userInput: ", userInput);

	var newWhitelist = await getJobWhitelist(userInput);

	// replace tagify "whitelist" array values with new values 
    // and add back the ones already choses as Tags
    jobTagify.settings.whitelist.push(...newWhitelist, ...jobTagify.value)

    // render the suggestions dropdown
    jobTagify.loading(false).dropdown.show.call(jobTagify);
    console.log("job whitelist: ", jobTagify.whitelist);
}

export async function softwareTagInput(e){
    // clear current whitelist
	softwareTagify.settings.whitelist.length = 0; // reset current whitelist
	// show loader & hide suggestions dropdown (if opened)
    softwareTagify.loading(true).dropdown.hide.call(softwareTagify)

    var userInput = e.detail.value;
	var newWhitelist = await getSoftwareWhitelist(userInput);

	// replace tagify "whitelist" array values with new values 
    // and add back the ones already choses as Tags
    softwareTagify.settings.whitelist.push(...newWhitelist, ...softwareTagify.value)

    // render the suggestions dropdown
    softwareTagify.loading(false).dropdown.show.call(softwareTagify);
    console.log("software whitelist: ", softwareTagify.whitelist);
}