console.log('JS Loaded');

function IndicateActive(){
    // let navItem = document.querySelectorAll('.nav-item');
    // console.log(navItem);

    document.querySelectorAll('.nav-item').forEach(navItem => {
        navItem.addEventListener('click', (e) => {
            let navItem = e.currentTarget.childNodes[1]; 
            console.log(navItem)
            navItem.classList.toggle('active')
        })
    })
    // navItem.addEventListener("click", (e) => {
    //     if (navItem.classList.contains('active')){
    //         navItem.classList.remove('active');        
    //     } else {
    //         navItem.classList.toggle('active')
    //     };
    // });
};
IndicateActive()
