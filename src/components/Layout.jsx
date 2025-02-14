import Header from "./Header";

const Layout = ({ children }) => {
  return (
    <div className="h-screen overflow-hidden bg-[#ECECEC] flex flex-col">
      <Header />
      {children}
    </div>
  );
};

export default Layout;
