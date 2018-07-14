﻿using System.Collections.Generic;

namespace COM3D2.MaidFiddler.Core.Service
{
    public partial class Service
    {
        private Dictionary<string, Dictionary<string, bool>> maidLockList = new Dictionary<string, Dictionary<string, bool>>();
        private Maid selectedMaid;

        private string selectedMaidGuid;

        public Dictionary<string, object> SelectActiveMaid(string guid)
        {
            selectedMaidGuid = guid;

            if (guid == null)
            {
                selectedMaid = null;
                return null;
            }

            selectedMaid = GetMaid(guid);
            return ReadMaidData(selectedMaid);
        }

        public void SetMaidPropertyActive(string property, object value)
        {
            if (selectedMaid == null)
                return;

            SetMaidProperty(selectedMaid, property, value);
        }

        public void SetPersonalActive(int personalId)
        {
            if (selectedMaid == null)
                return;

            SetPersonal(selectedMaid, personalId);
        }

        public void SetCurrentJobClassActive(object classId)
        {
            if (selectedMaid == null)
                return;

            SetCurrentJobClass(selectedMaid, classId);
        }

        public void SetCurrentYotogiClassActive(object classId)
        {
            if (selectedMaid == null)
                return;

            SetCurrentYotogiClass(selectedMaid, classId);
        }

        public void SetContractActive(int contract)
        {
            if (selectedMaid == null)
                return;

            SetContract(selectedMaid, contract);
        }

        public void SetCurSeikeikenActive(int seikeiken)
        {
            if (selectedMaid == null)
                return;

            SetCurSeikeiken(selectedMaid, seikeiken);
        }

        public void SetInitSeikeikenActive(int seikeiken)
        {
            if (selectedMaid == null)
                return;

            SetInitSeikeiken(selectedMaid, seikeiken);
        }

        public bool ToggleActiveMaidLock(string propertyName, bool value)
        {
            if (selectedMaid == null)
                return false;

            return TogglePropertyLock(selectedMaidGuid, propertyName, value);
        }

        internal void InitMaidList()
        {
            maidLockList.Clear();
            foreach (Maid maid in GameMain.Instance.CharacterMgr.GetStockMaidList())
            {
                var dict = new Dictionary<string, bool>();
                maidLockList[maid.status.guid] = dict;

                foreach (string setter in maidSetters.Keys)
                {
                    dict[setter] = false;
                }
            }
        }

        internal void AddMaid(Maid maid)
        {
            if (maidLockList == null)
                return;
            var dict = new Dictionary<string, bool>();
            maidLockList[maid.status.guid] = dict;

            foreach (string setter in maidSetters.Keys)
            {
                dict[setter] = false;
            }
        }

        internal void RemoveMaid(Maid maid)
        {
            maidLockList?.Remove(maid.status.guid);
        }
    }
}