// Enable footnote link support for pages with width < 1240.
function bind_footnote_links() {
    if ($(document).width() > 1240) {
        return;
    }
    let footnotes = $("div.footnotes").find("ol > li > p > a.reversefootnote");
    for (let i = 0; i < footnotes.length; i++) {
        let footnote = footnotes[i];
        footnote.addEventListener('click', function(e) {
            e.preventDefault();
            var target = $($(this).attr('href'));
            if (target.length) {
                $('div.body-inner').animate({
                    scrollTop: target.get(0).offsetTop,
                });
            }
        });
    }
}

// Toggle collapsible TOC headings in sidebar
function init_collapsible_toc() {
    const tocItems = document.querySelectorAll('.book-summary ul.summary li.chapter ul li');
    tocItems.forEach(li => {
        const subUl = li.querySelector('ul');
        if (subUl) {
            const textContent = li.textContent || '';
            if (textContent.includes('관련 함수')) {
                li.classList.add('collapsible-parent');
                
                // If active or contains active, expand it
                const hasActiveChild = li.classList.contains('active') || li.querySelector('.active');
                if (hasActiveChild) {
                    li.classList.add('expanded');
                }

                // Clicking toggles expansion
                li.addEventListener('click', function(e) {
                    e.stopPropagation();
                    li.classList.toggle('expanded');
                });
            }
        }
    });
}

function init_collapsible_category() {
    const categories = document.querySelectorAll('.book-summary ul.summary li.collapsible-category');
    categories.forEach(li => {
        // Toggle when clicking the area (like the arrow)
        li.addEventListener('click', function(e) {
            // Only toggle if clicked outside the <a> link itself
            if (e.target.tagName !== 'A') {
                e.stopPropagation();
                li.classList.toggle('expanded');
            }
        });
    });
}

function run_initializers() {
    bind_footnote_links();
    init_collapsible_toc();
    init_collapsible_category();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run_initializers);
} else {
    run_initializers();
}

// Re-initialize collapsible menus on dynamic AJAX page changes
if (typeof gitbook !== 'undefined') {
    gitbook.events.bind('page.change', function() {
        run_initializers();
    });
}
