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
    editTags:{
        keepInvalidTags: false,
        },
    dropdown:{
        enabled:2
        }
})

//Find user input in software question
var softwareInput = document.querySelector("input[id=software-text-input]");
softwareTagify = new Tagify (softwareInput, {
    enforceWhitelist: true,
    whitelist: []
});

// grab whitelist for job class tags from AJAX
async function getJobWhitelist(){
    return await $.ajax({
        type: "GET",
        url: "/get_job_classes",
    });
}

// grab whitelist for software tags from AJAX
async function getSoftwareWhitelist(){
    return await $.ajax({
        type: "GET",
        url: "/get_software",
    });
}


export async function jobTagInput(){
    // clear current whitelist
	jobTagify.settings.whitelist.length = 0; // reset current whitelist
	// show loader & hide suggestions dropdown (if opened)
    jobTagify.loading(true).dropdown.hide.call(jobTagify)

	var newWhitelist = await getJobWhitelist();

	// replace tagify "whitelist" array values with new values 
    // and add back the ones already choses as Tags
    jobTagify.settings.whitelist.push(...newWhitelist, ...jobTagify.value)

    // render the suggestions dropdown
    jobTagify.loading(false).dropdown.show.call(jobTagify);
}

export async function softwareTagInput(){
    // clear current whitelist
	softwareTagify.settings.whitelist.length = 0; // reset current whitelist
	// show loader & hide suggestions dropdown (if opened)
    softwareTagify.loading(true).dropdown.hide.call(softwareTagify)

	var newWhitelist = await getSoftwareWhitelist();

	// replace tagify "whitelist" array values with new values 
    // and add back the ones already choses as Tags
    softwareTagify.settings.whitelist.push(...newWhitelist, ...softwareTagify.value)

    // render the suggestions dropdown
    softwareTagify.loading(false).dropdown.show.call(softwareTagify);
}