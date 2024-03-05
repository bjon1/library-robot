const Mainbuttons = ({ image, link, name }) => {


    const goToLink = () => {
       window.location.href = link
    }
 
    return(
 
       <div>
          <a onClick={goToLink}>
             <img src={image}/>
          </a>
          <p>{name}</p>
       </div>
    )
 }
 
 export default Mainbuttons