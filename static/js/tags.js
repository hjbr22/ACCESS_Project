//Declare tagify variables
var jobTagify, softwareTagify;

/* #################################
!!! DO NOT USE JQUERY WITH TAGIFY !!! 
   ################################ */

//Collect whitelist from ajax call
var jobWhitelist = await getJobWhitelist();
var softwareWhitelist = await getSoftwareWhitelist();

//Find user input in job class question
var jobInput = document.querySelector("input[id=job-type-text-input]");
jobTagify = new Tagify (jobInput, {
    enforceWhitelist: true,
    whitelist: jobWhitelist,
    editTags: false,
    dropdown:{
        enabled: 0,
        maxItems: 10,
        }
})

//Find user input in software question
var softwareInput = document.querySelector("input[id=software-text-input]");
softwareTagify = new Tagify (softwareInput, {
    enforceWhitelist: true,
    whitelist: softwareWhitelist,
    editTags: false,
    dropdown: {
        enabled: 0,
        maxItems: 10
    }
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