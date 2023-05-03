document.addEventListener('DOMContentLoaded',()=>{
    let checkthegenre = document.querySelector('#option');
    checkthegenre.addEventListener('change',(event)=>{
        let value = event.target.value;
        let oldinput = document.querySelector('#file_form_creation');
        let oldbr = document.querySelector('.br_category');
        let oldbr2 = document.querySelector('#br_dance');
        let oldinput2 = document.querySelector('#file_form_thumbnail');
        let old_h4_thumbnail = document.querySelector('#thumbnailh4');
        if(oldinput !== null)
        {
            oldinput.remove();
            oldbr.remove();
            if(oldinput2 !== null)
            {
                oldinput2.remove();
                oldbr2.remove();
                old_h4_thumbnail.remove();
            }
        }
        let input = document.createElement('input');
        let br = document.createElement('br');
        br.className = "br_category";
        if(value == "Dance"||value == "Programming")
        {
            let br2 = document.createElement('br');
            br2.id = "br_dance";
            let input2 = document.createElement('input');
            let h4_thumbnail = document.createElement('h4');
            h4_thumbnail.id = "thumbnailh4";
            h4_thumbnail.innerHTML = "Thumbnail";
            input.type = "file";
            input.className = "form-control";
            input.id = "file_form_creation";
            input.name = "filecreation";
            input2.className = "form-control";
            input2.type = "text";
            input2.placeholder = "Enter your youtube url here.(The link must be unlisted or public)";
            input2.id = "file_form_thumbnail";
            input2.name = "thumbnail";
            document.querySelector('#category_form_place').append(input2);
            document.querySelector('#category_form_place').append(br);
            document.querySelector('#category_form_place').append(h4_thumbnail);
            document.querySelector('#category_form_place').append(input);
            document.querySelector('#category_form_place').append(br2);
        }
        else if(value == "Music"||value == "Illustration")
        {
            input.type = "file";
            input.className = "form-control";
            input.id = "file_form_creation";
            input.name = "filecreation";
            document.querySelector('#category_form_place').append(input);
            document.querySelector('#category_form_place').append(br);
        }
    })
    let seethegenre = document.querySelector('#option');
    let distinct = document.querySelector('#choose_category_header');
    if(distinct != null)
    {
        seethegenre.addEventListener('change',(event)=>{
            let value = event.target.value;
            location.replace(`http://127.0.0.1:8000/home${value}`);
        })
    }
   let inun = document.querySelectorAll('.inun_button');
   if(inun !== null)
    {
        fetch('/API_Interest')
        .then(response => response.json())
        .then(contents =>{
            for(let i=0;i<inun.length;i++){
                for(let j=0;j<contents.length;j++)
                {
                    if(inun[i].value == parseInt(contents[j].content_id))
                    {
                        inun[i].innerHTML = "Uninterest";
                        inun[i].id = "uninterest_button";
                    }
                }
            }
        })
    }
    let success_view = document.querySelectorAll('.success_view');
    let failed_view = document.querySelectorAll('.failed_view')
    if(inun !== null)
    {
        for(let i=0;i<inun.length;i++)
        {
            inun[i].addEventListener('click',()=>{
                if(inun[i].id === "uninterest_button")
                {
                    fetch('http://127.0.0.1:8000/API_Uninterest',{
                    method:'POST',
                    body:JSON.stringify({
                        Content_id:inun[i].value,
                        Category:document.querySelector('#choose_category_header').innerHTML
                    })
                    })
                    .then(response => response.json())
                    .then(result =>{
                        if(typeof result.success != "undefined")
                        {
                            success_view[i].style.display = 'block';
                            success_view[i].innerHTML = `${result.success}`;
                            failed_view[i].style.display = 'none';
                            inun[i].innerHTML = "Interest";
                            inun[i].id = "interest_button";
                        }
                        else if(typeof result.error != "undefined")
                        {
                            failed_view[i].style.display = 'block';
                            failed_view[i].innerHTML = `${result.error}`;
                            success_view[i].style.display = 'none';
                        }
                    })
                }
                else if(inun[i].id === "interest_button")
                {
                    fetch('http://127.0.0.1:8000/API_Interest',{
                    method:'POST',
                    body:JSON.stringify({
                        Content_id:inun[i].value,
                        Category:document.querySelector('#choose_category_header').innerHTML
                    })
                    })
                    .then(response => response.json())
                    .then(result =>{
                        if(typeof result.success != "undefined")
                        {
                            success_view[i].style.display = 'block';
                            success_view[i].innerHTML = `${result.success}`;
                            failed_view[i].style.display = 'none';
                            inun[i].innerHTML = "Uninterest";
                            inun[i].id = "uninterest_button";
                        }
                        else if(typeof result.error != "undefined")
                        {
                            failed_view[i].style.display = 'block';
                            failed_view[i].innerHTML = `${result.error}`;
                            success_view[i].style.display = 'none';
                        }
                    })
                }
            })
        }
    }
    let temp_notif = document.querySelectorAll('.notif_class');
    for(let i=0;i<temp_notif.length;i++)
    {
        temp_notif[i].addEventListener('click',()=>{
            fetch(`/API_Notif/${temp_notif[i].id}`,{
                method:'PUT',
                body:JSON.stringify({
                    seen:true
                })
            })
            temp_notif[i].remove();
        })
    }
});
