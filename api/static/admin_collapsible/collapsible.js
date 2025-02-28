(function ($) {
    $(document).on("formset:added", function (event, row, prefix) {
      collapseInlines(row);
    });
  
    $(document).ready(function () {
      collapseInlines(document);
    });
  
    function collapseInlines(container) {
      $(container)
        .find(".djn-inline-form")
        .each(function () {
          const title = $(this).find("h3:first");
          if (title.length) {
            if ($(this).data("collapsible")) return;
  
            title.css({
              background: "#f5f5f5",
              padding: "10px",
              border: "1px solid #ccc",
              cursor: "pointer",
            });
  
            const content = $(this).find(".djn-items");
            content.hide(); // Collapse by default
  
            const toggleBtn = $("<span> 🔽</span>");
            toggleBtn.css({
              cursor: "pointer",
              marginLeft: "10px",
              color: "#007BFF",
              fontWeight: "bold",
            });
  
            title.append(toggleBtn);
  
            title.on("click", function () {
              content.slideToggle(200);
              toggleBtn.text(content.is(":visible") ? " 🔼" : " 🔽");
            });
  
            $(this).data("collapsible", true);
          }
        });
    }
  })(django.jQuery);
  