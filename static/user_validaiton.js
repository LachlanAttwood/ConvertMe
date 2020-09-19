function update_file_selection() {
   /*  Modifies the "Choose file..." to the currently selected file.
   */
    path = document.getElementById('file_picker').value  // Gets the path
    document.styleSheets[1].addRule('.file-custom:after','content: "'+ path.replace(/.*[\/\\]/, '') +'";');
}


function validate_power_point(form) {
   /*  Submits the form on the condition that the file path is not
    *   empty and is a valid PowerPoint extension (.ppt or .pptx).
   */
    path = document.getElementById('file_picker').value  // Gets the path

    // Checks the path isn't empty and the text at the end (after a '.' character) is 'ppt' or 'pptx'
    if (path.length != 0 && (path.split('.')[path.split('.').length-1] == 'ppt' || path.split('.')[path.split('.').length-1] == 'pptx')) {
        form.submit() // Submits the form, performing conversion
    }
    else {
        alert("The submitted file was not valid.")
    }
}
