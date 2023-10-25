Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-dropzone",{
    url: "upload/",
    maxFiles: 1,
    maxFilesize: 1,
    acceptedFiles: '.png, .jpg'
});

var rangeSlider = function(){
    var slider = $('.slidecontainer'),
        range = $('.slider'),
        value = $('.range-slider__value');
      
    slider.each(function(){
  
      value.each(function(){
        var value = $(this).prev().attr('value');
        $(this).html(value);
      });
  
      range.on('input', function(){
        $(this).next(value).html(this.value);
      });
    });
  };
  
  rangeSlider();

  $(function() {
    $('input[id="thresholding"]').on('click', function() {
        
            $('#divSlider').show();
        
    });
  })

  $(function() {
    $('input[id="region_growing"]').on('click', function() {
        
            $('#divSlider').hide();
        
    });
  })

  $(function() {
    $('input[id="unet"]').on('click', function() {
        
            $('#divSlider').hide();
        
    });
  })