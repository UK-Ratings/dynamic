document.addEventListener("DOMContentLoaded", function() {
    var cardContent = document.querySelector('.home-scrollable-card-body');
    var scrollCount = 0;
    var maxScrollCount = 5;

    function scrollCard() {
        if (scrollCount < maxScrollCount) {
            var scrollHeight = cardContent.scrollHeight - cardContent.clientHeight;
            var scrollStep = scrollHeight / 200; // Smaller steps for smoother scrolling
            var scrollInterval = setInterval(function() {
                if (cardContent.scrollTop < scrollHeight) {
                    cardContent.scrollTop += scrollStep;
                } else {
                    clearInterval(scrollInterval);
                    scrollCount++;
                    setTimeout(scrollCard, 1000); // Wait 1 second before scrolling again
                }
            }, 50); // Shorter interval for smoother scrolling
        } else {
            // Reset scrollCount to repeat the scroll
            scrollCount = 0;
            cardContent.scrollTop = 0; // Reset to the top
            setTimeout(scrollCard, 1000); // Wait 1 second before starting again
        }
    }

    scrollCard();
});
