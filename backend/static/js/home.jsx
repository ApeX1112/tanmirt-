document.querySelectorAll('.item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.item').forEach(i => {
            i.classList.remove('selected');
        });
        this.classList.add('selected');
    });
});

document.querySelectorAll('.item').forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.transform = "translateY(-10px)";
    });
    item.addEventListener('mouseleave', function() {
        this.style.transform = "translateY(0)";
    });
});