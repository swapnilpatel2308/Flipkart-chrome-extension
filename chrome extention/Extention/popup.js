
function set_data(data){
  var tableContainer = document.getElementById("tableContainer");
  
  var table = document.createElement("table");


  for (var key in data) {
    if (data.hasOwnProperty(key)) {
      var row = document.createElement("tr");
      var cell1 = document.createElement("td");
      var cell2 = document.createElement("td");
      cell1.textContent = key;
      cell2.textContent = data[key];
      row.appendChild(cell1);
      row.appendChild(cell2);
      table.appendChild(row);
    }
  }

  tableContainer.appendChild(table);
}

document.addEventListener('DOMContentLoaded', function() {
  var heading = document.getElementById('heading');


  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    var link = tabs[0].url;
      const url = 'http://127.0.0.1:8000/';
      console.log(link)
      const data = {
        url : link,
        code: false,
        number: 50
      };

      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
        set_data(data)
        // heading.textContent = ''
        heading.style.display = 'none';
      })
      .catch(error => {
      });
   
  });
});

