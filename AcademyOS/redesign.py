from pathlib import Path
base=Path(__file__).resolve().parents[1]/'deliverables'
out=Path(__file__).resolve().parent
(out/'source').mkdir(exist_ok=True)
for name in ['build_blueprint.py','requirements.py','requirements.txt','verify_and_export.py','preview.py','package.py']:
    s=(base/'source'/name).read_text(encoding='utf-8')
    for old,new in [('CampusOS','AcademyOS'),('CAMPUSOS','ACADEMYOS'),('campusos','academyos')]:s=s.replace(old,new)
    if name=='build_blueprint.py':
        for old,new in [('#18243D','#203B36'),('#657188','#62726D'),('#6553D9','#256855'),('#EFEDFF','#E3EFE3'),('#F6F7FB','#F5F4EE'),('#E5E8F0','#DFE5DC'),('#087C67','#24694F'),('#E9F7F2','#E8F1E6'),('#1D2542','#203B36'),('#F0F2F8','#EBEFE7'),('#EEF0F6','#EAEDE4'),('#293253','#2E5248'),('#353C67','#416B5A'),('#514A9C','#749879'),('#CEC8FF','#D4EAC8'),('#DAD5FA','#CEE0BF')]:s=s.replace(old,new)
        s=s.replace("text('CAMPUS',48,25,12,PURPLE,'Bold');text('OS',99,25,12,INK,'Bold')", "text('AcademyOS',48,24,15,INK,'Bold')")
        s=s.replace('restrained violet accents','botanical green accents and editorial hierarchy').replace("('Lavender',LAV)","('Sage',LAV)")
        s=s.replace("rect(x,y,w,91,WHITE,11,LINE)","rect(x,y+2,w,91,'#E9ECE4',18)\n    rect(x,y,w,91,['#E3EFE3','#F4EBD9','#E6EDF1','#EEE8F1'][int((x-236)/207)%4],18)\n    circle(x+w-22,y+22,9,WHITE)\n    text('↗',x+w-22,y+15,10,PURPLE,'Bold','center')")
        s=s.replace("rect(x,y,w,h,WHITE,12,LINE)","rect(x,y+2,w,h,'#E9ECE4',18)\n    rect(x,y,w,h,WHITE,18)")
        s=s.replace("rect(x,y,w,32,PURPLE if primary else WHITE,7", "rect(x,y,w,32,PURPLE if primary else WHITE,16")
        s=s.replace("rect(48,166,164,530,NAV,14)","rect(48,166,164,530,'#EDF0E8',15)").replace('rect(198,166,14,530,NAV)',"rect(198,166,14,530,'#EDF0E8')")
        s=s.replace("text('campus',67,185,18,WHITE,'Bold');text('os',132,185,18,'#BEB4FF','Bold')", "circle(76,196,12,PURPLE);text('A',76,186,15,WHITE,'Bold','center');text('AcademyOS',95,186,15,INK,'Bold')")
        s=s.replace("rect(64,223,132,46,'#303855',8)","rect(64,223,132,46,WHITE,12)")
        s=s.replace("8.3,'#CDD4E5','Bold'","8.3,MUTED,'Bold'").replace("75,249,9.8,WHITE","75,249,9.8,INK")
        s=s.replace("'#514A87'","'#256855'").replace("'#BCB4F5' if l==nav else '#75809D'","'#D4EAC8' if l==nav else '#819188'")
        s=s.replace("WHITE if l==nav else '#C0C8DC'","WHITE if l==nav else MUTED")
        s=s.replace("line(65,635,195,635,'#424B67')","line(65,635,195,635,LINE)")
        s=s.replace("101,650,10,WHITE,'Bold'","101,650,10,INK,'Bold'").replace("101,667,9,'#AEB9D0'","101,667,9,MUTED")
        s=s.replace("rect(x-3,y-3,272,489,NAV,27)","rect(x-5,y-5,276,493,'#D5DFD4',32)\n    rect(x-3,y-3,272,489,NAV,30)")
        s=s.replace("rect(x,y,266,483,BG,24)","rect(x,y,266,483,'#EFF3E9',28)\n    c.saveState();c.setFillAlpha(.20);circle(x+210,y+130,72,'#C0D9B8');circle(x+48,y+300,65,'#E3CFB3');c.restoreState()\n    rect(x+99,y+9,68,17,INK,9)")
        s=s.replace("rect(x,y+432,266,51,WHITE,18)","c.saveState();c.setFillAlpha(.92);rect(x+8,y+432,250,43,WHITE,21);c.restoreState()\n    rect(x+103,y+478,60,3,INK,1)")
    (out/'source'/name).write_text(s,encoding='utf-8')
print(out)
