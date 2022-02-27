from time import sleep
from modules import Cells
import gspread
import schedule

gc = gspread.service_account()


def choose_mtf(word, row):
    works = {f'{word}{i}': sh.worksheet(f'{word}{i}').row_count for i in range(1, 20) if sh.worksheet(f'{word}{i}').acell(row).value != 'NEW'}
    min_key = min(works, key=works.get)
    worksheet = sh.worksheet(min_key)
    return worksheet.acell(row).value, min_key


# record_and_Regulators('12','ali','ag','1234','dabetan','fazapeyma','viber','1400','9728393','1400')


def check_status(cuscode, sheet):
    worksheet = sh.worksheet(sheet)
    cell = worksheet.find(cuscode)
    info = worksheet.row_values(cell.row)
    if 'T' in sheet:
        if info[12] == 'SET':
            transfer_to_mosahebe(info)
            schedule.cancel_job(f't{cuscode}')
        elif info[12] == 'cancel':
            schedule.cancel_job(f't{cuscode}')
    elif 'M' in sheet:
        sit = worksheet.acell(f'z{cell.row}').value
        if sit == 'DONE':
            transfer_to_froosh(info)
            schedule.cancel_job(f'm{cuscode}')
        elif sit == 'CLOSE':
            schedule.cancel_job(f'm{cuscode}')
    elif 'F' in sheet:
        sit = worksheet.acell(f'AV{cell.row}').value
        if sit == '':
            schedule.cancel_job(f'f{cuscode}')
        elif sit == 'CLOSE':
            schedule.cancel_job(f'f{cuscode}')


def record_and_SetRegulator(timestap, fname, lname, number, edu, target, familiarity, date, cuscode, deldate):
    [regName, sheet] = choose_mtf('T', 'k2')
    worksheet = sh.worksheet("LEADS")
    report_line = [timestap, fname, lname, number, edu, target, familiarity, date, cuscode, deldate, regName]
    worksheet.append_row(report_line)
    worksheet = sh.worksheet(sheet)
    worksheet.append_row(report_line)
    schedule.every(30).minutes.do(check_status, cuscode=cuscode, sheet=sheet).tag(f't{cuscode}')


def transfer_to_mosahebe(info):
    [m_name, sheet] = choose_mtf('M', 'x2')
    info.append(m_name)
    worksheet = sh.worksheet("SETs")
    worksheet.append_row(info)
    worksheet = sh.worksheet(sheet)
    worksheet.append_row(info)
    schedule.every(30).minutes.do(check_status, cuscode=info[8], sheet=sheet).tag(f'm{info[8]}')


def transfer_to_froosh(info):
    [f_name, sheet] = choose_mtf('F', 'AR2')
    info.append(f_name)
    worksheet = sh.worksheet('DONES')
    worksheet.append_row(info)
    worksheet = sh.worksheet(sheet)
    worksheet.append_row(info)
    schedule.every(30).minutes.do(check_status, cuscode=info[8], sheet=sheet).tag(f'f{info[8]}')


def add_row(info,start_row):
    j = 1
    for i in info:
        new_cells.append(gspread.Cell(start_row, j, i))
        j += 1


spread_id_record = ''
sheet_title_record = 'LEADS'

spread_id_mosahebe = ''
sheet_title_mosahebe = 'SETs'

spread_id_foroosh = ''
sheet_title_foroosh = 'DONES'

if __name__ == '__main__':
    # load sheet
    g_acc = gspread.service_account()
    sleep(1)
    sh = g_acc.open_by_key(spread_id)
    wks = None
    for i in range(10):
        sleep(1)
        try:
            wks = sh.worksheet(sheet_title)
            break
        except Exception as e:
            print(e)
        sleep(1)
    if wks is None:
        exit(1)

    # load cells
    row_count = len(wks.get())
    column_count = wks.col_count
    print(row_count, column_count)
    cells = Cells(wks.range(1, 1, row_count, column_count))
    new_cells = Cells([])
    # for i in header:
    #     print(i[0].value)
    # main()
    # r_cells = cells - new_cells

    if new_cells.cells:
        wks.batch_update(new_cells.export_for_batch_update())
