import sys
from colored import Fore,Back,Style
from datetime import datetime
from radboy.DB.db import *
from radboy.BNC.BnC import *
currency={}
currency['1$']=1
currency['2$']=2
currency['5$']=5
currency['10$']=10
currency['20$']=20
currency['50$']=50
currency['100$']=100
currency['penny']=0.01
currency['nickel']=0.05
currency['dime']=0.1
currency['quarter']=0.25

def brute_force(max_dollars=None,default_display_chunk=3000,display_chunk=None):
    print("disabled for now!")
    return
    now=datetime.now()
    if max_dollars == None:
        max_dollars=Prompt.__init2__(None,func=FormBuilderMkText,ptext="max dollars:",helpText="max dollars",data="float")
        if max_dollars in ['d',None]:
            return
        if display_chunk in [None,]:
            display_chunk=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"how many items before update to screen[default={default_display_chunk}]:",helpText="an integer for how many between print to screen",data="int")
            if display_chunk in [None,]:
                return
            elif display_chunk in ['d',]:
                display_chunk=default_display_chunk

    max_unit_range=int(max_dollars/currency['penny'])

    with Session(ENGINE) as session:
        possibilities=0
        ttl_found=0
        last=0
        for c001 in range(0,max_unit_range):
            check=session.query(CashPool).filter(and_(CashPool.Name=='Penny',CashPool.Qty<=0)).first()
            if check:
                if (possibilities%(display_chunk))==0:
                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                    last=len(msg)
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                possibilities+=1
                break
            if c001*0.01 > max_dollars:
                if (possibilities%(display_chunk))==0:
                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                    last=len(msg)
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                possibilities+=1
                break
            check=session.query(CashPool).filter(and_(CashPool.Name=='Penny')).first()
            if check:
                if check.Qty < c001:
                    if (possibilities%(display_chunk))==0:
                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                        last=len(msg)
                        sys.stdout.write(msg)
                        sys.stdout.flush()
                    possibilities+=1
                    break

            for c005 in range(0,max_unit_range):
                check=session.query(CashPool).filter(and_(CashPool.Name=='Nickel',CashPool.Qty<=0)).first()
                if check:
                    if (possibilities%(display_chunk))==0:
                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                        last=len(msg)
                        sys.stdout.write(msg)
                        sys.stdout.flush()
                    possibilities+=1
                    break
                check=session.query(CashPool).filter(and_(CashPool.Name=='Nickel')).first()
                if check:
                    if check.Qty < c005:
                        if (possibilities%(display_chunk))==0:
                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                            last=len(msg)
                            sys.stdout.write(msg)
                            sys.stdout.flush()
                            possibilities+=1
                        break

                if c005*0.05 > max_dollars:
                    if (possibilities%(display_chunk))==0:
                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                        last=len(msg)
                        sys.stdout.write(msg)
                        sys.stdout.flush()
                    possibilities+=1
                    break
                for c010 in range(0,max_unit_range):
                    check=session.query(CashPool).filter(and_(CashPool.Name=='Dime',CashPool.Qty<=0)).first()
                    if check:
                        if (possibilities%(display_chunk))==0:
                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                            last=len(msg)
                            sys.stdout.write(msg)
                            sys.stdout.flush()
                        possibilities+=1
                        break
                    check=session.query(CashPool).filter(and_(CashPool.Name=='Dime')).first()
                    if check:
                        if check.Qty < c010:
                            if (possibilities%(display_chunk))==0:
                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                last=len(msg)
                                sys.stdout.write(msg)
                                sys.stdout.flush()
                            possibilities+=1
                            break

                    if c010*0.1 > max_dollars:
                        if (possibilities%(display_chunk))==0:
                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                            last=len(msg)
                            sys.stdout.write(msg)
                            sys.stdout.flush()
                        possibilities+=1
                        break
                    for c025 in range(0,max_unit_range):
                        check=session.query(CashPool).filter(and_(CashPool.Name=='Quarter',CashPool.Qty<=0)).first()
                        if check:
                            if (possibilities%(display_chunk))==0:
                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                last=len(msg)
                                sys.stdout.write(msg)
                                sys.stdout.flush()
                            possibilities+=1
                            break
                        check=session.query(CashPool).filter(and_(CashPool.Name=='Quarter')).first()
                        if check:
                            if check.Qty < c025:
                                if (possibilities%(display_chunk))==0:
                                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                    last=len(msg)
                                    sys.stdout.write(msg)
                                    sys.stdout.flush()
                                possibilities+=1
                                break                        
                        if c025*0.25 > max_dollars:
                            if (possibilities%(display_chunk))==0:
                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                last=len(msg)
                                sys.stdout.write(msg)
                                sys.stdout.flush()
                            possibilities+=1
                            break
                        for d1 in range(0,max_unit_range):
                            check=session.query(CashPool).filter(and_(CashPool.Name=='1$Bill',CashPool.Qty<=0)).first()
                            if check:
                                if (possibilities%(display_chunk))==0:
                                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                    last=len(msg)
                                    sys.stdout.write(msg)
                                    sys.stdout.flush()
                                possibilities+=1
                                break
                            check=session.query(CashPool).filter(and_(CashPool.Name=='1$Bill')).first()
                            if check:
                                if check.Qty < d1:
                                    if (possibilities%(display_chunk))==0:
                                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                        last=len(msg)
                                        sys.stdout.write(msg)
                                        sys.stdout.flush()
                                    possibilities+=1
                                    break                        
                            if d1*1 > max_dollars:
                                if (possibilities%(display_chunk))==0:
                                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                    last=len(msg)
                                    sys.stdout.write(msg)
                                    sys.stdout.flush()
                                possibilities+=1
                                break

                            for d2 in range(0,max_unit_range):
                                check=session.query(CashPool).filter(and_(CashPool.Name=='2$Bill',CashPool.Qty<=0)).first()
                                if check:
                                    if (possibilities%(display_chunk))==0:
                                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                        last=len(msg)
                                        sys.stdout.write(msg)
                                        sys.stdout.flush()
                                    possibilities+=1
                                    break
                                check=session.query(CashPool).filter(and_(CashPool.Name=='2$Bill')).first()
                                if check:
                                    if check.Qty < d2:
                                        if (possibilities%(display_chunk))==0:
                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                            last=len(msg)
                                            sys.stdout.write(msg)
                                            sys.stdout.flush()
                                        possibilities+=1
                                        break
                                if d2*2 > max_dollars:
                                    if (possibilities%(display_chunk))==0:
                                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                        last=len(msg)
                                        sys.stdout.write(msg)
                                        sys.stdout.flush()
                                    possibilities+=1
                                    break
                                for d5 in range(0,max_unit_range):
                                    check=session.query(CashPool).filter(and_(CashPool.Name=='5$Bill',CashPool.Qty<=0)).first()
                                    if check:
                                        if (possibilities%(display_chunk))==0:
                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                            last=len(msg)
                                            sys.stdout.write(msg)
                                            sys.stdout.flush()
                                        possibilities+=1
                                        break
                                    check=session.query(CashPool).filter(and_(CashPool.Name=='5$Bill')).first()
                                    if check:
                                        if check.Qty < d5:
                                            if (possibilities%(display_chunk))==0:
                                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                last=len(msg)
                                                sys.stdout.write(msg)
                                                sys.stdout.flush()
                                            possibilities+=1
                                            break                                    
                                    if d5*5 > max_dollars:
                                        if (possibilities%(display_chunk))==0:
                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                            last=len(msg)
                                            sys.stdout.write(msg)
                                            sys.stdout.flush()
                                        possibilities+=1
                                        break
                                    for d10 in range(0,max_unit_range):
                                        check=session.query(CashPool).filter(and_(CashPool.Name=='10$Bill',CashPool.Qty<=0)).first()
                                        if check:
                                            if (possibilities%(display_chunk))==0:
                                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                last=len(msg)
                                                sys.stdout.write(msg)
                                                sys.stdout.flush()
                                            possibilities+=1
                                            break
                                        check=session.query(CashPool).filter(and_(CashPool.Name=='10$Bill')).first()
                                        if check:
                                            if check.Qty < d10:
                                                if (possibilities%(display_chunk))==0:
                                                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                    last=len(msg)
                                                    sys.stdout.write(msg)
                                                    sys.stdout.flush()
                                                possibilities+=1
                                                break
                                        if d10*10 > max_dollars:
                                            if (possibilities%(display_chunk))==0:
                                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                last=len(msg)
                                                sys.stdout.write(msg)
                                                sys.stdout.flush()
                                            possibilities+=1
                                            break
                                        for d20 in range(0,max_unit_range):
                                            check=session.query(CashPool).filter(and_(CashPool.Name=='20$Bill',CashPool.Qty<=0)).first()
                                            if check:
                                                if (possibilities%(display_chunk))==0:
                                                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                    last=len(msg)
                                                    sys.stdout.write(msg)
                                                    sys.stdout.flush()
                                                possibilities+=1
                                                break
                                            check=session.query(CashPool).filter(and_(CashPool.Name=='20$Bill')).first()
                                            if check:
                                                if check.Qty < d20:
                                                    if (possibilities%(display_chunk))==0:
                                                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                        last=len(msg)
                                                        sys.stdout.write(msg)
                                                        sys.stdout.flush()
                                                    possibilities+=1
                                                    break
                                            if d20*20 > max_dollars:
                                                if (possibilities%(display_chunk))==0:
                                                    msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                    last=len(msg)
                                                    sys.stdout.write(msg)
                                                    sys.stdout.flush()
                                                possibilities+=1
                                                break
                                            for d50 in range(0,max_unit_range):
                                                check=session.query(CashPool).filter(and_(CashPool.Name=='50$Bill',CashPool.Qty<=0)).first()
                                                if check:
                                                    if (possibilities%(display_chunk))==0:
                                                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                        last=len(msg)
                                                        sys.stdout.write(msg)
                                                        sys.stdout.flush()
                                                    possibilities+=1
                                                    break
                                                check=session.query(CashPool).filter(and_(CashPool.Name=='50$Bill')).first()
                                                if check:
                                                    if check.Qty < d50:
                                                        if (possibilities%(display_chunk))==0:
                                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                            last=len(msg)
                                                            sys.stdout.write(msg)
                                                            sys.stdout.flush()
                                                        possibilities+=1
                                                        break
                                                if d50*50 > max_dollars:
                                                    if (possibilities%(display_chunk))==0:
                                                        msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                        last=len(msg)
                                                        sys.stdout.write(msg)
                                                        sys.stdout.flush()
                                                    possibilities+=1
                                                    break
                                                for d100 in range(0,max_unit_range):
                                                    check=session.query(CashPool).filter(and_(CashPool.Name=='100$Bill',CashPool.Qty<=0)).first()
                                                    if check:
                                                        if (possibilities%(display_chunk))==0:
                                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                            last=len(msg)
                                                            sys.stdout.write(msg)
                                                            sys.stdout.flush()
                                                        possibilities+=1
                                                        break
                                                    check=session.query(CashPool).filter(and_(CashPool.Name=='100$Bill')).first()
                                                    if check:
                                                        if check.Qty < d100:
                                                            if (possibilities%(display_chunk))==0:
                                                                msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                                last=len(msg)
                                                                sys.stdout.write(msg)
                                                                sys.stdout.flush()
                                                            possibilities+=1
                                                            break                                                    
                                                    if d100*100 > max_dollars:
                                                        if (possibilities%(display_chunk))==0:
                                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                            last=len(msg)
                                                            sys.stdout.write(msg)
                                                            sys.stdout.flush()
                                                        possibilities+=1
                                                        break
                                                    formula_string=f"""({currency['1$']}*{d1})+({currency['2$']}*{d2})+({currency['5$']}*{d5})+({currency['10$']}*{d10})+({currency['20$']}*{d20})+({currency['50$']}*{d50})+({currency['100$']}*{d100})+({currency['penny']}*{c001})+({currency['nickel']}*{c005})+({currency['dime']}*{c010})+({currency['quarter']}*{c025})"""
                                                    print(formula_string)
                                                    test=eval(formula_string)
                                                    taken=datetime.now()-now
                                                    if round(test,2) == round(max_dollars,2):
                                                        msg=f'{"\b"*last}'+f'{Fore.light_green}Found {ttl_found} out of {possibilities} Iterations @ {now}, taking {taken} to find!{Style.reset}'
                                                        last=len(msg)
                                                        sys.stdout.write(msg)
                                                        sys.stdout.flush()
                                                        ttl_found+=1
                                                        yield formula_string,round(test,2)
                                                    else:
                                                        if (possibilities%(display_chunk))==0:
                                                            msg=f'{"\b"*last}'+f'{Fore.light_yellow}|{datetime.now().strftime("%H:%M:%S-%m/%d/%Y")}|{datetime.now()-now}|{possibilities}{Style.reset}'
                                                            last=len(msg)
                                                            sys.stdout.write(msg)
                                                            sys.stdout.flush()
                                                    possibilities+=1



