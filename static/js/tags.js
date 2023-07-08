//Declare tagify variables
export var jobTagify, softwareTagify;

/* #################################
!!! DO NOT USE JQUERY WITH TAGIFY !!! 
   ################################ */

//Collect whitelist from ajax call
var jobWhitelist = await getJobWhitelist();
var softwareWhitelist = await getSoftwareWhitelist();

//Add "Other" option to whitelists
jobWhitelist.push("Other");
softwareWhitelist.push("Other");

//Find user input in job class question
var jobInput = document.querySelector("input[id=job-type-text-input]");
jobTagify = new Tagify (jobInput, {
    enforceWhitelist: true,
    whitelist: jobWhitelist,
    editTags: false,
    dropdown:{
        enabled: 0,
        maxItems: 10,
        highlightFirst: true
        }
});

//Create tagify input for "add job classes" question
var addJobInput = document.querySelector("input[id=job-type-add-tag]");
var addJobTagify = new Tagify(addJobInput, {
    blacklist: jobWhitelist
});

//Find user input in software question
var softwareInput = document.querySelector("input[id=software-text-input]");
softwareTagify = new Tagify (softwareInput, {
    enforceWhitelist: true,
    whitelist: softwareWhitelist,
    editTags: false,
    dropdown: {
        enabled: 0,
        maxItems: 10,
        highlightFirst: true
    }
});

//Create tagify input for "add software/packages" question
var addSoftwareInput = document.querySelector("input[id=software-libraries-add-tag]");
var addSoftwareTagify = new Tagify(addSoftwareInput, {
    blacklist: softwareWhitelist
});

// grab whitelist for job class tags via AJAX
async function getJobWhitelist(){
    return await $.ajax({
        type: "GET",
        url: "/get_job_classes",
    });
}

// grab whitelist for software tags via AJAX
async function getSoftwareWhitelist(){
    return await $.ajax({
        type: "GET",
        url: "/get_software",
    });
}

export function jobNoMatches(){
    jobTagify.suggestedListItems = ["Other"];
}

export function softwareNoMatches(){
    softwareTagify.suggestedListItems = ["Other"];
}

export function hideAddJob(e){
    console.log("added tag:", e.detail.data.value);
    if (e.detail.data.value.toLowerCase() === "other"){
        $(".hide-add-job").removeClass('d-none').show();
    }
}

export function showAddJob(e){
    if (e.detail.data.value.toLowerCase() === "other"){
        $(".hide-add-job").addClass('d-none').hide()
    }
}

export function hideAddSoftware(e){
    console.log("added tag:", e.detail.data.value);
    if (e.detail.data.value.toLowerCase() === "other"){
        $(".hide-add-software").removeClass('d-none').show();
    }
}

export function showAddSoftware(e){
    if (e.detail.data.value.toLowerCase() === "other"){
        $(".hide-add-software").addClass('d-none').hide()
    }
}