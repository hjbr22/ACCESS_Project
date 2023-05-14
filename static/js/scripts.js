$(document).ready(function(){

    // ACCESS RPs
    const RPs = [['aces',"ACES (Texas A&M)"], ["anvil","Anvil (Purdue)"], ["bridges","Bridges-2 (PSC)"],
                 ["darwin","DARWIN (Delaware)"], ["delta","Delta (NCSA)"], ["expanse","Expanse (SDSC)"],
                 ["faster","FASTER (SDSC)"], ["jetstream","Jetsteram2 (IU)"], ["ookami","OOKAMI (Stonybrook)"],
                 ["kyric","KyRIC (Kentucky)"], ["rockfish","Rockfish (JHU)"], ["stampede","Stampede-2 (TACC)"],
                 ["osg","Open Science Grid (OSG)"], ["osn","Open Storage Network (OSN)"]]

    // populate the experience with ACCESS providers options
    for (let i = 0; i < RPs.length; i++){
        $("#access-rps").append(
            $(`<div class="form-check">
                <input class="form-check-input" type="checkbox" id="${RPs[i][0]}-option" value="${RPs[i][0]}">
                <label class="form-check-label" for="${RPs[i][0]}-option">${RPs[i][1]}</label> 
               </div>`)
        )
    }

    // fields of research
    const fields = ["Biology", "Chemistry", "Physics", "Computer Science", "Civil Engineering", "Economics",
                    "Linguistics", "History", "Agriculture", "Medicine"].sort()

    // populate the field of research dropdown
    for (let i = 0; i < fields.length; i++){
        $("#field-dropdown-options").append(
            $(`<div class="form-check dropdown-item">
            <input class="form-check-input" type="checkbox" id="${fields[i].split(' ').join('-').toLocaleLowerCase()}-option" value="">
            <label class="form-check-label" for="${fields[i].split(' ').join('-').toLowerCase()}-option">${fields[i]}</label> 
            </div>`)
        )
    }

    // search the field of research dropdown
    $("#field-dropdown-search").on("keyup", function(){
        var value = $(this).val().toLowerCase();
        $("#field-dropdown-options .dropdown-item").filter(function(){
            $(this).toggle(($(this).text().toLowerCase().indexOf(value)>-1))
        })
    })

    // types of jobs
    const jobType = ["Data Analytics", "Data Mining", "NLP", "Textual Analysis", "Modeling and Simulation", "Bioinformatics",
                     "Biophysics", "Biochemistry", "Fluid Dynamics", "Materials Science", "Image Processing", "Machine Learning",
                     "Astronomic Science", "Digital Humanities", "Compuational Chemistry", "Genomics", "Deep Learning", "High Energy Physics",
                     "Virtual Machine", "General", "Parallel"]
    
    // autocomplete for selecting types of jobs
    $("#job-type-text-input").autocomplete({
        source: jobType,
        select: function(event, ui){
            $('#job-type-tag-container').append(
                `<div class="tag" style="display: inline-block; margin: 2px;">
                    <span class="badge badge-primary">
                        ${ui.item.value}
                        <a class="remove-tag" style="cursor:pointer; color: white; margin-left: 5px;">x</a>
                    </span>
                </div>`)
            this.value='';
            return false;
        }
    })
        
    // remove the from job types when 'x' is clicked
    $(document).on('click', '.remove-tag', function(){
        $(this).parents('.tag').remove()
    })



});