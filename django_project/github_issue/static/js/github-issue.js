//noinspection JSUnusedGlobalSymbols
window.submitIssue = function () {
  $("#issue-submit-button").attr("disabled", "disabled");
  $.post("/github-issue", {
    'title': $("#issue-title").val(), 'desc': $("#issue-description").val() })
  .done(function() {
    $('#issue-modal').removeClass('is-active');
    $("#issue-submit-button").removeAttr("disabled");
  })
  .fail(function() {
    $('#issue-modal').removeClass('is-active');
    alert('Issue not submitted, configuration error!');
    $("#issue-submit-button").removeAttr("disabled");
  })
}
