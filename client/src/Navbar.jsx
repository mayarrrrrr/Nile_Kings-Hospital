import './index.css'

function Navbar(){

    const links = [
        {name:"ABOUT",link:"/",color:"text-green-800"},
        {name:"PATIENT'S PORTAL",link:"/",color:"text-custom-purple"},
        {name:"SERVICES ",link:"/"}
        
        
    ]

    return(
        <>
        <div className='shadow-md w-full fixed top-0 left-0 '>
            
            <div className='md:flex bg-white pt-3 '>
                <div className='font-bold cursor-pointer items-center flex items-center font-[Poppins] text-2xl  '>

                    <img src="/public/hospital_logo.jpeg" className='w-20 mr-2 ml-10 '/> 
                    <span className='mt-0'>NILE KINGS SPECIALIST HOSPITAL </span>
                </div>
                <br></br>
                
            </div>
            <hr className="border-t-1 border-black w-1/2 ms-40" />
            <ul className='md:flex md:items-center  ms-40 text-2xl font-[Poppins] me-10  '>
                    {
                        links.map((link)=>(
                            <li key={link.name} className='md:ml-10'>
                                <a href={link.link} className={`${
                                    link.name === 'ABOUT' ? 'text-green-800' :
                                    link.name === "PATIENT'S PORTAL" ? 'text-custom-purple' :
                                     'text-black'
                                    } hover:text-purple-700`} >{link.name}</a>
                                
                            </li>
                        )) 
                    }
                </ul>
        </div>
        </>
    )

}
export default Navbar;