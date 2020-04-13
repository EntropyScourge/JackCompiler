import CompilationEngine as ce

a = ce.CompilationEngine('''class thing 
{
    method void CallSub(int x, char y, boolean h, int l, otherType q) 
    {
        var int u, v;
        var int i, sum;
        
        let length = Keyboard.readInt("HOW MANY NUMBERS? ");
        let u = 6;
    } 
}''', '')
a.compileClass()