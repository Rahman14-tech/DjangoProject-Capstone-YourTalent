document.addEventListener('DOMContentLoaded',()=>{
    let inun = document.querySelector('.inun_button');
    if(inun !== null)
    {
        inun.addEventListener('click',()=>{
            if(inun.id === "uninterest_button")
            {
                fetch('/API_Uninterest',{
                method:'POST',
                body:JSON.stringify({
                    Content_id:inun.value,
                    Category:document.querySelector('#The_category').innerHTML
                })
                })
                .then(response => response.json())
                .then(result =>{
                    if(typeof result.success != "undefined")
                    {
                        document.querySelector('#success_view').style.display = 'block';
                        document.querySelector('#success_view').innerHTML = `${result.success}`;
                        document.querySelector('#failed_view').style.display = 'none';
                        inun.innerHTML = "Interest";
                        inun.id = "interest_button";
                    }
                    else if(typeof result.error != "undefined")
                    {
                        document.querySelector('#failed_view').style.display = 'block';
                        document.querySelector('#failed_view').innerHTML = `${result.error}`;
                        document.querySelector('#success_view').style.display = 'none';
                    }
                })
            }
            else if(inun.id === "interest_button")
            {
                fetch('/API_Interest',{
                method:'POST',
                body:JSON.stringify({
                    Content_id:inun.value,
                    Category:document.querySelector('#The_category').innerHTML
                })
                })
                .then(response => response.json())
                .then(result =>{
                    if(typeof result.success != "undefined")
                    {
                        document.querySelector('#success_view').style.display = 'block';
                        document.querySelector('#success_view').innerHTML = `${result.success}`;
                        document.querySelector('#failed_view').style.display = 'none';
                        inun.innerHTML = "Uninterest";
                        inun.id = "uninterest_button";
                    }
                    else if(typeof result.error != "undefined")
                    {
                        document.querySelector('#failed_view').style.display = 'block';
                        document.querySelector('#failed_view').innerHTML = `${result.error}`;
                        document.querySelector('#success_view').style.display = 'none';
                    }
                })
            }
        })
    }
    let delete_contentcreator_content = document.querySelectorAll('.delete_contentcreator_content');
    let the_creatorname = document.querySelector('#the_creatorname').innerHTML;
    let category_globs = ""
    for(let i=0;i<delete_contentcreator_content.length;i++)
    {
        delete_contentcreator_content[i].addEventListener('click',()=>{
            category_globs = delete_contentcreator_content[i].value
            fetch(`/API_Delete/${delete_contentcreator_content[i].value}/${delete_contentcreator_content[i].id}`,{
                method:'PUT',
                body:JSON.stringify({
                    id:delete_contentcreator_content[i].id,
                    category:delete_contentcreator_content[i].value
                })
            })
            location.replace(`http://127.0.0.1:8000/mycontents/${the_creatorname}?category=${category_globs}`);
        })
    } 
})
