function copyMe(id){
  var copyText = document.getElementById(id);
  console.log(copyText);
  let previousValue = copyText.value;
  let newValue = (window.location.href).substring(0, window.location.href.length-1) + previousValue;
  console.log(newValue);

  const elementForCopy = document.createElement("textarea");
  elementForCopy.value = newValue;
  document.body.appendChild(elementForCopy);
  //copyText.value = newValue;
  elementForCopy.select();
  elementForCopy.setSelectionRange(0, 99999);
  document.execCommand("copy", false);
  document.body.removeChild(elementForCopy);
}
