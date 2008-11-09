$(function()
{
  $("#menu-photo-list a").click(function()
  {
    var imageSource = $(this).attr("href");
    var desc = $(this).children("img").attr("alt");
    
    showImage(imageSource,desc);
    return false;
  });
});

function showImage(src,desc)
{
$("#photo-big").addClass("loading");
$("#photo-big img").fadeOut("slow")
  .remove();
$("#photo-big p").fadeOut("slow")
  .remove();
var largeImage = new Image();
$(largeImage).attr("src", src)
  .attr("alt", desc)
  .load(function()
{
  $(largeImage).hide();
  $("#photo-big").removeClass("loading")
    .append(largeImage);
  $(largeImage).fadeIn("slow");
  $(largeImage).after("<p class='photo-text'>"+desc+"</p>");
}
	);
}

function slideshow(startidx)
{
var photo = photos[startidx];
  $("#slideshow img").remove();
  var largeImage = new Image();
  $(largeImage).attr("src", photo)
    .load(function()
    {
      $(largeImage).hide();
      $("#slideshow").append(largeImage);
      $(largeImage).fadeIn("slow");
    }
);

if (startidx == photos.length - 1)
{
     startidx = 0;
}
 else 
   {
     startidx = startidx + 1;
   }
setTimeout("slideshow("+startidx+")", speed);
}
