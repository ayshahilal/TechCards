function flipCard(card) {
    card.classList.add('flipped');
  }
  
  function flipBack(card) {
    card.classList.remove('flipped');
  }
  
  function save_score(event, card_id, score, mixed){
      event.stopPropagation();
    
      fetch(`/select_score/${card_id}/${score}/${mixed}`)
     .then(response => response.json())
     .then(result => {
          document.getElementById("self_score").innerHTML = `Score: ${result.data}`;
          window.location.href = result.url;
  
         fetch(`/solved_progress/${card_id}/${mixed}`)
          .then(response => response.json())
          .then(result => {
              document.getElementById("show_progress").innerHTML = `${result.data.solved_cards_count}/${result.data.all_cards_count}`;
      });
     });
  }
  
  
  function open_delete_option(event, card_id){
      event.stopPropagation();
      document.querySelector(`#delete_card_${card_id}`).style.display = "block";
      document.querySelector(`#delete_option_${card_id}`).style.display = "none";
      document.querySelector(`#edit_option_${card_id}`).style.display = "none";
  }
  
  function close_delete_form(event, card_id){
      event.stopPropagation();
      document.querySelector(`#delete_card_${card_id}`).style.display = "none";
      document.querySelector(`#delete_option_${card_id}`).style.display = "block";
      document.querySelector(`#edit_option_${card_id}`).style.display = "block";
  }
  
  function set_not_solved(event, card_id){
      event.stopPropagation();
      fetch(`/set_not_solved/${card_id}`)
     .then(response => response.json())
     .then(result => {
          document.querySelector(`#flash_card_${card_id}`).style.display = "none"; 
          window.location.href = result.url;
          console.log(result.message);
     });
  }
  