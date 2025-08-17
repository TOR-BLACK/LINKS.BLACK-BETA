import { DVInstruction } from "@/types/dtos";
import DVInstructionItem from "./DVInstructionItem";

interface DVInstructionsProps {
  instructions: DVInstruction[]; // Массив инструкций, содержащих заголовок и строки с текстом/изображениями
}

export default function DVInstructions({ instructions }: DVInstructionsProps) {
  return (
    <div className="accordion tools"> {/* Контейнер для списка инструкций */}
      {instructions.map((item) => (
        <DVInstructionItem instruction={item} key={item.id} /> // Отображаем каждую инструкцию с уникальным ключом
      ))}
    </div>
  );
}