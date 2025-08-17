import HeaderScroll from "./HeaderScroll";
import HeaderContent from "./HeaderContent";
import HeaderMobile from "./HeaderMobile";

export default function Header() {
  return (
    <>
      <header className="header">
        <HeaderContent />
      </header>
      <HeaderScroll />
      <HeaderMobile />
    </>
  );
}
