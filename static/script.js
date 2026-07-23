async function uploadFile(){


let file =
document.getElementById("csvFile").files[0];



if(!file){

alert("Please select CSV file");

return;

}



let formData =
new FormData();



formData.append(
"file",
file
);




let response =
await fetch(
"/predict_file",
{

method:"POST",

body:formData

}

);




let result =
await response.json();



console.log(result);




if(result.error){


document.getElementById("result").innerHTML =

`

<h3>Error</h3>

<p>
${result.error}
</p>

`;

return;


}





// Statistics


document.getElementById("result").innerHTML =


`

<h2>
${result.message}
</h2>


<p>
Total Transactions:
${result.total_transactions}
</p>


<p>
Fraud Transactions:
${result.fraud_transactions}
</p>


<p>
Normal Transactions:
${result.normal_transactions}
</p>


<p>
Fraud Percentage:
${result.fraud_percentage}%
</p>

`;







// Fraud table


let fraudTable =

document.querySelector(
"#fraudTable tbody"
);



fraudTable.innerHTML="";



result.fraud_records.forEach(

transaction=>{


let row =
document.createElement("tr");



row.innerHTML =

`

<td>

${transaction.Amount}

</td>



<td>

${transaction.Fraud_Probability}%

</td>


`;



fraudTable.appendChild(row);



}

);







// SHAP table


let shapTable =

document.querySelector(
"#shapTable tbody"
);



shapTable.innerHTML="";



result.shap_explanation.forEach(

item=>{


let row =
document.createElement("tr");



row.innerHTML =

`

<td>

${item.Feature}

</td>



<td>

${item.Impact.toFixed(5)}

</td>


`;



shapTable.appendChild(row);



}

);







// =========================
// FRAUD PIE CHART
// =========================


let oldChart =
Chart.getChart("fraudChart");


if(oldChart){

oldChart.destroy();

}



new Chart(

document.getElementById("fraudChart"),

{

type:"pie",


data:{


labels:[

"Fraud Transactions",

"Normal Transactions"

],



datasets:[{


data:[

result.fraud_transactions,

result.normal_transactions

]


}]


},



options:{


responsive:true


}


}

);







// =========================
// FRAUD PROBABILITY BAR CHART
// =========================



let oldBar =
Chart.getChart("probabilityChart");


if(oldBar){

oldBar.destroy();

}




new Chart(

document.getElementById("probabilityChart"),

{


type:"bar",


data:{


labels:

result.fraud_records.map(

item=>item.Amount

),



datasets:[{


label:"Fraud Probability %",



data:

result.fraud_records.map(

item=>item.Fraud_Probability

)


}]


},



options:{


responsive:true,


scales:{


y:{


beginAtZero:true,


max:100


}


}


}


}


);



}