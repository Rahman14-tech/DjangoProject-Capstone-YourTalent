document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('form').onsubmit = () =>{
        document.querySelector('#register_contain').style.display = 'none';
        document.querySelector('#loading_register_div').style.display = 'block';
    }
})