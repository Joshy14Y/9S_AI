
export const Title = ({ text }) => {
    return (
        <div className="w-full flex flex-col justify-center ">
            <h2 className="text-5xl sm:text-7xl md:text-8xl lg:text-9xl uppercase text-center 
            text-gray-500/10 font-bold">
                {text}
            </h2>
            <h2 className="text-2xl -top-[2rem] sm:text-4xl sm:-top-[2.7rem] md:text-5xl md:-top-[3.5rem] 
            lg:text-6xl lg:-top-[4.3rem] font-medium uppercase text-center align-bottom 
            m-0 relative text-gray-200">
                {text}
            </h2>
        </div>
    )
}