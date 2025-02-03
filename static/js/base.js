
// Toggle chevron rotation on click
$('.nav-link.has-chevron').on('click', function () {
    $(this).find('.fa-chevron-right').toggleClass('rotate-down');
});


// Toggle sidebar, topbar, and main content on hamburger button click
$('#hamburger-btn').on('click', function () {
    $('#sidebar, #topbar, #mainContent').toggleClass('collapsed');
});

$(document).on('click', '#hamburger-btn', function () {
    setTimeout(function () {
        $('table.dataTable').each(function () {
            if ($.fn.DataTable.isDataTable(this)) {
                $(this).DataTable().draw();
            }
        });
    }, 300);
});


function delayLoading(divId) {
    $(divId).css('visibility', 'hidden'); // Hide initially
    setTimeout(function() {
        $(divId).css('visibility', '').hide().fadeIn(300); // Reset visibility and apply fade-in
    }, 200);
}


// Function to expand sidebar
function expandSidebar() {
    if ($('#sidebar').hasClass('collapsed')) {
        $('#sidebar, #mainContent, #topbar').removeClass('collapsed');
    }
}

// Function to collapse sidebar
function collapseSidebar() {
    if (!$('#sidebar').hasClass('collapsed')) {
        $('#sidebar, #mainContent, #topbar').addClass('collapsed');
    }
}

var hoverTimer;
var delay = 100;

/* // Mouseover event with delay for sidebar expansion
$('#hamburger-btn').on('mouseover', function () {
    if ($('#sidebar').hasClass('collapsed') && $(window).width() < 961) {
        hoverTimer = setTimeout(expandSidebar, delay);
    }
});

// Mouseout event to cancel the action if mouse leaves early
$('#hamburger-btn').on('mouseout', function () {
    clearTimeout(hoverTimer);
});
 */

// Collapse sidebar when the mouse leaves the sidebar
$('#sidebar').on('mouseleave', function () {
    if ($(window).width() < 961) {
        collapseSidebar();
    }
});

// Toggle sidebar based on window resize
$(window).on('resize', function () {
    if ($(window).width() < 961) {
        collapseSidebar();
    } else {
        expandSidebar();
    }
});



/* 

// Function to execute after delay
function expandSidebar() {
    if (sidebar.classList.contains('collapsed')) {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('collapsed');
        topbar.classList.remove('collapsed');
    }
}


// Mouseover event with delay
hamburgerBtn.addEventListener('mouseover', function() {
    if (sidebar.classList.contains('collapsed') & ($(window).width() < 961)) {
        hoverTimer = setTimeout(expandSidebar, delay);
    }
});

// Mouseout event to cancel the action if mouse leaves early
hamburgerBtn.addEventListener('mouseout', function() {
    clearTimeout(hoverTimer);
}); */



$(document).ready(function() {
    if ($(window).width() < 961) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('collapsed');
        topbar.classList.add('collapsed');
    }
    /* // Placeholder on search bar
    $('.dt-search .dt-input').attr('placeholder', 'Search...');

    // Select the input element
    var $input = $('.dt-search .dt-input');
    $input.css('padding-left', '35px');

    // Create the input group wrapper
    var $inputGroup = $('<div>', { class: 'input-icon' });
    $inputGroup.css('max-width', $input.outerWidth());

    
    // Create the addon (optional: for icon, text, or button)
    var $iconAddon = $(
        '<span class="input-icon-addon"><i class="fa-solid fa-search mx-0"></i></span>'
    );
    // Add the input and addon to the wrapper
    $input.wrap($inputGroup); // Wrap the input
    $input.before($iconAddon); // Insert the addon before the input */




    // Function to dismiss alert when clicking outside of it
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.alert').length) {
            $('.alert-dismissable').alert('close');
        }
    });
    // Optional: prevent the alert from closing when clicking inside it
    $('.alert').on('click', function(event) {
        event.stopPropagation();
    });

    $("#error-modal-reload-btn").on("click", function(){
        location.reload();
    });


});


$(document).ready(function () {
    function updateRestrictedDisplay() {
        const isActive = $('#toggle-restricted-btn').hasClass('active');
        if (isActive) {
            $('.restricted').addClass('show-restricted');
        } else {
            $('.restricted').removeClass('show-restricted');
        }
    }

    // Event listener for toggle button
    $(document).on('click', '#toggle-restricted-btn', function () {
        $(this).toggleClass('active');
        updateRestrictedDisplay(); 
    });

    // Reapply visibility logic when new elements are added via HTMX
    document.addEventListener('htmx:afterSwap', function () {
        updateRestrictedDisplay(); 
    });
});
